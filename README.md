# Proyecto 2 — CI-0141 Bases de Datos Avanzadas

ETL que integra los datos de la encuesta de énfasis (CSV, base de datos
relacional mock y API/JSON mock) en un Data Warehouse PostgreSQL con modelo
estrella, para análisis en Metabase.

## Requisitos

- Docker + Docker Compose
- Python 3.11+
- `pip install -r requirements.txt`

## 1. Levantar la base de datos (Data Warehouse)

```bash
docker compose up -d dw
```

Esto inicia un contenedor de PostgreSQL (`ecci_dw`) y ejecuta automáticamente
los scripts de `sql/ddl/` (esquemas `staging` y `dw`, dimensiones, hechos,
vistas y seeds) en el primer arranque.

Verificar que esté listo:

```bash
docker compose exec dw pg_isready -U etl_user -d ecci_dw
```

> El puerto publicado está definido en `docker-compose.yml` (actualmente
> `5434:5432`). Si usás un puerto distinto a 5432, exportá `POSTGRES_PORT`
> antes de correr el ETL (ver siguiente sección).

Para reiniciar desde cero (borra todos los datos y vuelve a correr los DDL):

```bash
docker compose down -v
docker compose up -d dw
```

## 2. Configuración del ETL

El ETL lee la configuración de variables de entorno (`etl/config.py`):

| Variable | Default |
|---|---|
| `POSTGRES_HOST` | `localhost` |
| `POSTGRES_PORT` | `5432` |
| `POSTGRES_DB` | `ecci_dw` |
| `POSTGRES_USER` | `etl_user` |
| `POSTGRES_PASSWORD` | `etl_pass` |

Ejemplo si el contenedor publica el puerto `5434`:

```bash
export POSTGRES_PORT=5434
```

## 3. Correr el ETL completo

```bash
python -m etl.main
```

Pasos ejecutados en orden (`etl/main.py` → `ETL_STEPS`):

1. `relational_setup_mock_source` — crea/llena `public.external_db` a partir
   de `preprocessed_data/encuesta_enfasis_external_db.sql` (mock de la fuente
   relacional on-premise).
2. `clean_raw_staging` — vacía `staging.encuesta_enfasis_raw`.
3. `csv_to_raw_staging` — carga `preprocessed_data/encuesta_enfasis.csv` →
   `staging.encuesta_enfasis_raw` (fuente `CSV`).
4. `relational_extract_to_staging` — copia `public.external_db` →
   `staging.encuesta_enfasis_raw` (fuente `BD_RELACIONAL`).
5. `json_extract_to_staging` — carga
   `preprocessed_data/encuesta_enfasis.json` → `staging.encuesta_enfasis_raw`
   (fuente `API`).
6. `load_dim_tiempo` — genera `dw.dim_tiempo` a partir de las fechas de
   envío/inicio presentes en staging.
7. `load_facts` — limpia (full reload) y reconstruye todas las tablas
   de hechos de `dw` desde staging, normalizando los valores, y registra la
   corrida en `dw.fact_auditoria`.

## 4. Estructura de `etl/`

```
etl/
├── config.py               # configuración (env vars) y conexión a Postgres
├── main.py                 # orquestador: corre ETL_STEPS en orden
├── extract/
│   ├── common.py           # columnas compartidas (SOURCE_COLUMNS) + lookup de id_fuente
│   ├── clean_staging.py    # limpieza de staging antes de extraer
│   ├── csv_source.py       # extract del CSV a staging
│   ├── relational_source.py# setup del mock relacional + extract a staging
│   └── json_source.py      # extract del mock JSON/API a staging
├── transform/
│   └── normalize.py        # parsers puros + mapeos columna→dimensión (testeable sin BD)
└── load/
    ├── dim_tiempo.py       # genera la dimensión tiempo desde staging
    └── facts.py            # full reload de las tablas de hechos + auditoría
```

## 5. Probar los extractores individualmente

Cada extractor es una función `(EtlConfig) -> None` y puede correrse aislado
desde un shell de Python. Esto es útil para depurar una sola fuente sin
re-ejecutar todo el pipeline.

```bash
python - <<'EOF'
from etl.config import load_config
from etl.extract import clean_staging, csv_source, relational_source, json_source
from etl.load import dim_tiempo, facts

config = load_config()

clean_staging.run(config)                       # limpia staging
csv_source.run(config)                          # extrae fuente CSV
relational_source.setup_mock_source(config)     # crea public.external_db
relational_source.extract_to_staging(config)    # extrae fuente BD_RELACIONAL
json_source.extract_to_staging(config)          # extrae fuente API (JSON)
dim_tiempo.run(config)                           # pobla dw.dim_tiempo
facts.run(config)                                # transforma + carga los hechos
EOF
```

Cada función imprime cuántas filas insertó. Los extractores son **idempotentes**
(borran primero las filas previas de esa misma fuente por `id_fuente` +
`archivo_origen`); la carga de hechos hace **full reload** (trunca y reconstruye).

### Validar los resultados en la base

Conteo por fuente en staging:

```bash
docker compose exec dw psql -U etl_user -d ecci_dw -c "
  SELECT id_fuente, archivo_origen, count(*)
  FROM staging.encuesta_enfasis_raw
  GROUP BY id_fuente, archivo_origen;
"
```

Resultado esperado tras correr el pipeline completo:

| id_fuente | archivo_origen | count |
|---|---|---|
| 1 (CSV) | `encuesta_enfasis.csv` | 269 |
| 2 (BD_RELACIONAL) | `encuesta_enfasis_external_db.sql` | 238 |
| 3 (API) | `encuesta_enfasis.json` | 96 |

Los `id_fuente` provienen de `dw.dim_fuente_datos` (ver `sql/ddl/03_seeds.sql`).

Hechos cargados y auditoría de la última corrida:

```bash
docker compose exec dw psql -U etl_user -d ecci_dw -c "
  SELECT count(*) AS respuestas FROM dw.fact_respuesta;
  SELECT estado, registros_insertados, registros_rechazados
  FROM dw.fact_auditoria ORDER BY id_auditoria;
"
```

## 6. Servicios adicionales

```bash
docker compose up -d metabase
```

Metabase queda disponible en [http://localhost:3000](http://localhost:3000),
conectado al Data Warehouse (`dw`) para dashboards.
