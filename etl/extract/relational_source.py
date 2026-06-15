"""Extract: mocked on-premise relational source (SQL Server stand-in)."""

from __future__ import annotations

from etl.config import EtlConfig
from etl.extract.common import SOURCE_COLUMNS, TARGET_TABLE, get_source_id


SETUP_SQL_FILE = "preprocessed_data/encuesta_enfasis_external_db.sql"
SOURCE_TYPE = "BD_RELACIONAL"
SOURCE_TABLE = "public.external_db"
ORIGIN_FILE = "encuesta_enfasis_external_db.sql"


def setup_mock_source(config: EtlConfig) -> None:
    """Create and populate the mocked relational source (public.external_db)."""

    import psycopg

    sql_path = config.repo_root / SETUP_SQL_FILE
    sql = sql_path.read_text(encoding="utf-8")

    with psycopg.connect(**config.connection_kwargs()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

    print(
        f"Created mocked external db in {config.db_name}.public.external_db "
        f"from {sql_path.relative_to(config.repo_root)}"
    )


def extract_to_staging(config: EtlConfig) -> None:
    """Copy rows from public.external_db into staging.encuesta_enfasis_raw."""

    import psycopg

    target_columns = ["id_fuente", "archivo_origen", *SOURCE_COLUMNS]
    select_columns = ",\n            ".join(f"{column}::TEXT" for column in SOURCE_COLUMNS)
    insert_sql = f"""
        INSERT INTO {TARGET_TABLE} (
            {", ".join(target_columns)}
        )
        SELECT
            %s,
            %s,
            {select_columns}
        FROM {SOURCE_TABLE}
    """

    with psycopg.connect(**config.connection_kwargs()) as conn:
        with conn.cursor() as cur:
            source_id = get_source_id(cur, SOURCE_TYPE)
            cur.execute(
                f"DELETE FROM {TARGET_TABLE} WHERE id_fuente = %s AND archivo_origen = %s",
                (source_id, ORIGIN_FILE),
            )
            cur.execute(insert_sql, (source_id, ORIGIN_FILE))
            inserted = cur.rowcount
        conn.commit()

    print(f"Loaded {inserted} rows from {SOURCE_TABLE} into {TARGET_TABLE}")
