"""Extract: JSON/API mock source (preprocessed_data/encuesta_enfasis.json)."""

from __future__ import annotations

import json

from etl.config import EtlConfig
from etl.extract.common import SOURCE_COLUMNS, TARGET_TABLE, get_source_id


SOURCE_TYPE = "API"
JSON_FILE = "preprocessed_data/encuesta_enfasis.json"
ORIGIN_FILE = "encuesta_enfasis.json"


def _to_text(value: object) -> str | None:
    """Cast a JSON scalar to TEXT for the raw staging table."""

    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def extract_to_staging(config: EtlConfig) -> None:
    """Load records from the JSON/API mock source into staging.encuesta_enfasis_raw."""

    import psycopg

    json_path = config.repo_root / JSON_FILE
    records = json.loads(json_path.read_text(encoding="utf-8"))

    target_columns = ["id_fuente", "archivo_origen", *SOURCE_COLUMNS]
    placeholders = ", ".join(["%s"] * len(target_columns))
    insert_sql = f"""
        INSERT INTO {TARGET_TABLE} (
            {", ".join(target_columns)}
        )
        VALUES ({placeholders})
    """

    with psycopg.connect(**config.connection_kwargs()) as conn:
        with conn.cursor() as cur:
            source_id = get_source_id(cur, SOURCE_TYPE)
            cur.execute(
                f"DELETE FROM {TARGET_TABLE} WHERE id_fuente = %s AND archivo_origen = %s",
                (source_id, ORIGIN_FILE),
            )
            rows = [
                (
                    source_id,
                    ORIGIN_FILE,
                    *(_to_text(record.get(column)) for column in SOURCE_COLUMNS),
                )
                for record in records
            ]
            cur.executemany(insert_sql, rows)
        conn.commit()

    print(f"Loaded {len(records)} rows from {json_path.relative_to(config.repo_root)} into {TARGET_TABLE}")
