from __future__ import annotations

from datetime import date

from etl.config import EtlConfig
from etl.transform.normalize import parse_fecha

TARGET_TABLE = "dw.dim_tiempo"
STAGING_TABLE = "staging.encuesta_enfasis_raw"

# date.weekday(): 0 = Monday ... 6 = Sunday
_DIAS_SEMANA = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
]


def _row_for(fecha: date) -> tuple[date, int, int, int, str, int]:
    trimestre = (fecha.month - 1) // 3 + 1
    return (
        fecha,
        fecha.year,
        fecha.month,
        fecha.day,
        _DIAS_SEMANA[fecha.weekday()],
        trimestre,
    )


def run(config: EtlConfig) -> None:
    """Generate dim_tiempo rows for every distinct submission/start date."""

    import psycopg

    insert_sql = f"""
        INSERT INTO {TARGET_TABLE} (fecha, año, mes, dia, dia_semana, trimestre)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (fecha) DO NOTHING
    """

    with psycopg.connect(**config.connection_kwargs()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT submitted_at FROM {STAGING_TABLE}
                UNION
                SELECT started_at FROM {STAGING_TABLE}
                """
            )
            fechas = {
                fecha
                for (raw,) in cur.fetchall()
                if (fecha := parse_fecha(raw)) is not None
            }
            cur.executemany(insert_sql, [_row_for(fecha) for fecha in sorted(fechas)])
            inserted = cur.rowcount
        conn.commit()

    print(f"Loaded {inserted} distinct dates into {TARGET_TABLE}")
