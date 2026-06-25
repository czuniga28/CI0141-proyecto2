from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from etl.config import EtlConfig
from etl.transform import normalize as nz

STAGING_TABLE = "staging.encuesta_enfasis_raw"

# Synthetic offset for the 2021 responses that have no source response_id.
_SYNTHETIC_SRC_OFFSET = 900_000

_FACT_TABLES = [
    "dw.fact_canal_comunicacion",
    "dw.fact_factor_decision",
    "dw.fact_calificacion_actividad",
    "dw.fact_dificultad_semestre",
    "dw.fact_dominio_conocimiento",
    "dw.fact_habilidad_blanda",
    "dw.fact_respuesta",
]

_INSERT_RESPUESTA = """
    INSERT INTO dw.fact_respuesta (
        id_respuesta_src, id_ciclo, id_tiempo_envio, id_tiempo_inicio,
        id_enfasis, id_semestre_decision, id_fuente,
        asistio, influyo_actividades, razon_no_asistio, razon_decision,
        comentario_poco_util, comentario_le_gusto, comentario_a_mejorar,
        comentario_general, pagina_alcanzada, idioma,
        tiempo_total_seg, tiempo_info_general_seg, tiempo_retro_seg,
        archivo_origen
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id_ciclo, id_respuesta_src) DO NOTHING
    RETURNING id_respuesta_sk
"""


def _lookup(cur, query: str) -> dict:
    """Return a {natural_key: surrogate_key} map for a dimension."""

    cur.execute(query)
    return {row[0]: row[1] for row in cur.fetchall()}


def _build_respuesta_values(row: dict, lookups: dict) -> tuple | None:
    """Resolve FKs and normalize a single fact_respuesta row.

    Returns ``None`` if the row cannot be tied to a cycle (id_ciclo is
    mandatory), which means it is rejected.
    """

    ciclo_key = nz.ciclo_nombre(row.get("term"), row.get("year"))
    id_ciclo = lookups["ciclo"].get(ciclo_key)
    if id_ciclo is None:
        return None

    response_id = nz.parse_int(row.get("response_id"))
    if response_id is None:
        response_id = _SYNTHETIC_SRC_OFFSET + row["id_staging"]

    fecha_envio = nz.parse_fecha(row.get("submitted_at"))
    fecha_inicio = nz.parse_fecha(row.get("started_at"))

    return (
        response_id,
        id_ciclo,
        lookups["tiempo"].get(fecha_envio),
        lookups["tiempo"].get(fecha_inicio),
        lookups["enfasis"].get(nz.emphasis_code(row.get("chosen_emphasis"))),
        lookups["semestre"].get(nz.clean_text(row.get("decision_semester"))),
        row["id_fuente"],
        nz.parse_si_no(row.get("attended")),
        nz.clean_text(row.get("activities_influenced")),
        nz.clean_text(row.get("no_attendance_reason")),
        nz.clean_text(row.get("decision_reason")),
        nz.clean_text(row.get("low_usefulness_comment")),
        nz.clean_text(row.get("liked_most")),
        nz.clean_text(row.get("liked_least_improve")),
        nz.clean_text(row.get("study_plan_comment")),
        nz.parse_int(row.get("last_page")),
        nz.clean_text(row.get("language")),
        nz.parse_numeric(row.get("time_total")),
        nz.parse_numeric(row.get("time_general_group")),
        nz.parse_numeric(row.get("time_feedback_group")),
        row.get("archivo_origen"),
    )


def _collect_children(row: dict, sk: int, lookups: dict, buffers: dict) -> None:
    """Append the bridge/Likert fact rows for one response to the buffers."""

    for col, canal in nz.HEARD_TO_CANAL.items():
        if nz.is_si(row.get(col)):
            buffers["canal"].append((sk, lookups["canal"][canal]))

    for col, factor in nz.FACTOR_TO_DIM.items():
        if nz.is_si(row.get(col)):
            buffers["factor"].append((sk, lookups["factor"][factor]))
    if nz.clean_text(row.get("factor_other")):
        buffers["factor"].append((sk, lookups["factor"][nz.FACTOR_OTHER_DIM]))

    for useful_col, impact_col, actividad in nz.ACTIVITY_RATINGS:
        utilidad = nz.parse_likert(row.get(useful_col))
        impacto = nz.parse_impacto(row.get(impact_col)) if impact_col else None
        if utilidad is not None or impacto is not None:
            buffers["actividad"].append(
                (sk, lookups["actividad"][actividad], impacto, utilidad)
            )

    for col, numero in nz.DIFFICULTY_TO_BLOQUE.items():
        dificultad = nz.parse_likert(row.get(col))
        if dificultad is not None:
            buffers["dificultad"].append((sk, lookups["bloque"][numero], dificultad))

    for suffix, area in nz.AXIS_TO_AREA.items():
        dominio = nz.parse_likert(row.get(f"axis1_{suffix}"))
        ensenanza = nz.parse_likert(row.get(f"axis2_{suffix}"))
        if dominio is not None or ensenanza is not None:
            buffers["dominio"].append((sk, lookups["area"][area], dominio, ensenanza))

    for col, habilidad in nz.SKILL_TO_HABILIDAD.items():
        mejora = nz.parse_likert(row.get(col))
        if mejora is not None:
            buffers["habilidad"].append((sk, lookups["habilidad"][habilidad], mejora))


def _flush_children(cur, buffers: dict) -> None:
    """Bulk-insert all buffered bridge/Likert fact rows."""

    inserts = {
        "canal": "INSERT INTO dw.fact_canal_comunicacion (id_respuesta_sk, id_canal) "
        "VALUES (%s, %s) ON CONFLICT DO NOTHING",
        "factor": "INSERT INTO dw.fact_factor_decision (id_respuesta_sk, id_factor) "
        "VALUES (%s, %s) ON CONFLICT DO NOTHING",
        "actividad": "INSERT INTO dw.fact_calificacion_actividad "
        "(id_respuesta_sk, id_actividad, impacto, utilidad) "
        "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
        "dificultad": "INSERT INTO dw.fact_dificultad_semestre "
        "(id_respuesta_sk, id_bloque, dificultad) "
        "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
        "dominio": "INSERT INTO dw.fact_dominio_conocimiento "
        "(id_respuesta_sk, id_area, dominio_propio, efectividad_ensenanza) "
        "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
        "habilidad": "INSERT INTO dw.fact_habilidad_blanda "
        "(id_respuesta_sk, id_habilidad, mejora) "
        "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
    }
    for key, sql in inserts.items():
        if buffers[key]:
            cur.executemany(sql, buffers[key])


def _record_auditoria(cur, started: datetime, counters: dict) -> None:
    """Write one EXITOSO audit row per source processed."""

    finished = datetime.now()
    for id_fuente, tally in counters.items():
        cur.execute(
            """
            INSERT INTO dw.fact_auditoria (
                id_fuente, fecha_inicio, fecha_fin, estado,
                registros_procesados, registros_insertados, registros_rechazados
            )
            VALUES (%s, %s, %s, 'EXITOSO', %s, %s, %s)
            """,
            (
                id_fuente,
                started,
                finished,
                tally["procesados"],
                tally["insertados"],
                tally["rechazados"],
            ),
        )


def _record_failure(config: EtlConfig, started: datetime, error: str) -> None:
    """Best-effort FALLIDO audit row in its own transaction."""

    import psycopg

    try:
        with psycopg.connect(**config.connection_kwargs()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id_fuente FROM dw.dim_fuente_datos ORDER BY id_fuente LIMIT 1"
                )
                row = cur.fetchone()
                if row is None:
                    return
                cur.execute(
                    """
                    INSERT INTO dw.fact_auditoria (
                        id_fuente, fecha_inicio, fecha_fin, estado, mensaje_error
                    )
                    VALUES (%s, %s, %s, 'FALLIDO', %s)
                    """,
                    (row[0], started, datetime.now(), error[:1000]),
                )
            conn.commit()
    except Exception:  # pragma: no cover - audit logging must not mask the cause
        pass


def run(config: EtlConfig) -> None:
    """Rebuild every dw fact table from staging."""

    import psycopg
    from psycopg.rows import dict_row

    started = datetime.now()
    counters: dict[int, dict[str, int]] = defaultdict(
        lambda: {"procesados": 0, "insertados": 0, "rechazados": 0}
    )

    conn = psycopg.connect(**config.connection_kwargs())
    try:
        with conn.cursor(row_factory=dict_row) as read_cur:
            read_cur.execute(f"SELECT * FROM {STAGING_TABLE} ORDER BY id_staging")
            staging_rows = read_cur.fetchall()

        with conn.cursor() as cur:
            lookups = {
                "ciclo": _lookup(cur, "SELECT ciclo_nombre, id_ciclo FROM dw.dim_ciclo"),
                "tiempo": _lookup(cur, "SELECT fecha, id_tiempo FROM dw.dim_tiempo"),
                "enfasis": _lookup(cur, "SELECT codigo, id_enfasis FROM dw.dim_enfasis"),
                "semestre": _lookup(
                    cur, "SELECT descripcion, id_semestre FROM dw.dim_semestre_carrera"
                ),
                "canal": _lookup(cur, "SELECT nombre, id_canal FROM dw.dim_canal"),
                "factor": _lookup(
                    cur, "SELECT nombre, id_factor FROM dw.dim_factor_decision"
                ),
                "actividad": _lookup(
                    cur, "SELECT nombre, id_actividad FROM dw.dim_actividad"
                ),
                "bloque": _lookup(
                    cur, "SELECT numero_ciclo, id_bloque FROM dw.dim_bloque_semestral"
                ),
                "area": _lookup(
                    cur, "SELECT nombre, id_area FROM dw.dim_area_conocimiento"
                ),
                "habilidad": _lookup(
                    cur, "SELECT nombre, id_habilidad FROM dw.dim_habilidad_blanda"
                ),
            }

            cur.execute(f"TRUNCATE {', '.join(_FACT_TABLES)} RESTART IDENTITY CASCADE")

            buffers: dict[str, list] = {
                key: []
                for key in ("canal", "factor", "actividad", "dificultad", "dominio", "habilidad")
            }

            for row in staging_rows:
                id_fuente = row["id_fuente"]
                counters[id_fuente]["procesados"] += 1

                values = _build_respuesta_values(row, lookups)
                if values is None:
                    counters[id_fuente]["rechazados"] += 1
                    continue

                cur.execute(_INSERT_RESPUESTA, values)
                returned = cur.fetchone()
                if returned is None:  # duplicate (id_ciclo, id_respuesta_src)
                    counters[id_fuente]["rechazados"] += 1
                    continue

                counters[id_fuente]["insertados"] += 1
                _collect_children(row, returned[0], lookups, buffers)

            _flush_children(cur, buffers)
            _record_auditoria(cur, started, counters)

        conn.commit()
    except Exception as exc:
        conn.rollback()
        _record_failure(config, started, str(exc))
        raise
    finally:
        conn.close()

    total_in = sum(t["insertados"] for t in counters.values())
    total_rej = sum(t["rechazados"] for t in counters.values())
    print(
        f"Loaded {total_in} responses into dw fact tables "
        f"({total_rej} rejected) from {len(counters)} sources"
    )
