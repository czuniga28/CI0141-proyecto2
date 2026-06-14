"""Shared configuration and utilities for ETL modules"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EtlConfig:
    """Runtime settings"""

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    repo_root: Path

    def connection_kwargs(self, *, dbname: str | None = None) -> dict[str, str | int]:
        return {
            "host": self.db_host,
            "port": self.db_port,
            "dbname": dbname or self.db_name,
            "user": self.db_user,
            "password": self.db_password,
        }


def load_config() -> EtlConfig:
    """Load ETL configuration from environment variables."""

    repo_root = Path(__file__).resolve().parents[1]

    return EtlConfig(
        db_host=os.getenv("POSTGRES_HOST", "localhost"),
        db_port=int(os.getenv("POSTGRES_PORT", "5432")),
        db_name=os.getenv("POSTGRES_DB", "ecci_dw"),
        db_user=os.getenv("POSTGRES_USER", "etl_user"),
        db_password=os.getenv("POSTGRES_PASSWORD", "etl_pass"),
        repo_root=repo_root,
    )
