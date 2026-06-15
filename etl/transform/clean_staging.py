"""Clean raw staging tables before loading source data."""

from __future__ import annotations

from etl.config import EtlConfig
from etl.extract.common import TARGET_TABLE


def run(config: EtlConfig) -> None:
    """Remove existing rows from raw staging."""

    import psycopg

    with psycopg.connect(**config.connection_kwargs()) as conn:
        with conn.cursor() as cur:
            cur.execute(f"TRUNCATE TABLE {TARGET_TABLE} RESTART IDENTITY")
        conn.commit()

    print(f"Cleaned {TARGET_TABLE}")
