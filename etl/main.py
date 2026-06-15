"""Central ETL orchestrator"""

from __future__ import annotations

import sys
from collections.abc import Callable

from etl import (
    clean_staging,
    external_db,
    load_csv_to_staging,
    load_external_to_staging,
)
from etl.config import EtlConfig, load_config
from etl.extract import json_source, relational_source
from etl.transform import clean_staging


EtlStep = tuple[str, Callable[[EtlConfig], None]]


ETL_STEPS: list[EtlStep] = [
    ("relational_setup_mock_source", relational_source.setup_mock_source),
    ("clean_raw_staging", clean_staging.run),
    ("csv_to_raw_staging", load_csv_to_staging.run),
    ("external_db_to_raw_staging", load_external_to_staging.run),
    # Future source modules can be added here:
    # ("json_source", load_json_source.run),
    ("relational_extract_to_staging", relational_source.extract_to_staging),
    ("json_extract_to_staging", json_source.extract_to_staging),
    # Future source modules can be added here:
    # ("csv_extract_to_staging", csv_source.extract_to_staging),
]


def run_all() -> None:
    """Run all configured ETL steps in order"""

    config = load_config()

    for step_name, step in ETL_STEPS:
        print(f"Starting ETL step: {step_name}")
        step(config)
        print(f"Finished ETL step: {step_name}")


def main() -> int:
    try:
        run_all()
    except Exception as exc:
        print(f"ETL failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
