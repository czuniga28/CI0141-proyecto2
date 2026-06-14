"""Module for creating a mocked external db in our own database."""

from __future__ import annotations

from etl.config import EtlConfig


SQL_FILE = "preprocessed_data/encuesta_enfasis_external_db.sql"


def run(config: EtlConfig) -> None:
    """Execute the PostgreSQL script to create the external_db schema and load the data"""

    import psycopg

    sql_path = config.repo_root / SQL_FILE
    sql = sql_path.read_text(encoding="utf-8")

    with psycopg.connect(**config.connection_kwargs()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

    print(
        f"Created mocked external db in {config.db_name}.public.external_db "
        f"from {sql_path.relative_to(config.repo_root)}"
    )
