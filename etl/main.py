"""Central ETL orchestrator"""

from __future__ import annotations

import sys
from collections.abc import Callable

from etl import external_db
from etl.config import EtlConfig, load_config


EtlStep = tuple[str, Callable[[EtlConfig], None]]


ETL_STEPS: list[EtlStep] = [
    ("external_db", external_db.run),
    # Future source modules can be added here:
    # ("csv_source", load_csv_source.run),
    # ("json_source", load_json_source.run),
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
