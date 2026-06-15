"""Load the consolidated CSV source into raw staging."""

from __future__ import annotations

import csv
from collections.abc import Iterator
from pathlib import Path

from etl.config import EtlConfig

SOURCE_TYPE = "CSV"
SOURCE_FILE = "preprocessed_data/encuesta_enfasis.csv"
TARGET_TABLE = "staging.encuesta_enfasis_raw"

STAGING_COLUMNS = [
    "term",
    "year",
    "response_id",
    "submitted_at",
    "started_at",
    "last_action_at",
    "last_page",
    "language",
    "seed",
    "heard_email",
    "heard_web",
    "heard_social",
    "heard_element",
    "heard_teachers",
    "heard_peers",
    "heard_other",
    "heard_facebook",
    "heard_telegram",
    "attended",
    "no_attendance_reason",
    "decision_semester",
    "activities_influenced",
    "decision_reason",
    "factor_professors",
    "factor_courses",
    "factor_ecci_events",
    "factor_advanced_students",
    "factor_study_plan",
    "factor_salary",
    "factor_job_market",
    "factor_other",
    "impact_intro_talk",
    "impact_student_roundtable",
    "impact_cc_industry_talk",
    "impact_iti_industry_talk",
    "impact_is_industry_talk",
    "impact_admin_myths_talk",
    "useful_intro_talk",
    "useful_student_roundtable",
    "useful_cc_industry_talk",
    "useful_iti_industry_talk",
    "useful_is_industry_talk",
    "useful_admin_myths_talk",
    "useful_admin_talk",
    "useful_cc_qa",
    "useful_cc_fusion",
    "useful_is_inside",
    "useful_is_google",
    "useful_iti_expectation",
    "useful_iti_security",
    "useful_iti_lora",
    "useful_iti_jobs",
    "low_usefulness_comment",
    "liked_most",
    "liked_least_improve",
    "chosen_emphasis",
    "difficulty_cycle_1",
    "difficulty_cycle_2",
    "difficulty_cycle_3",
    "difficulty_cycle_4",
    "axis1_programming",
    "axis2_programming",
    "axis1_discrete_structures",
    "axis2_discrete_structures",
    "axis1_architecture",
    "axis2_architecture",
    "axis1_assembly",
    "axis2_assembly",
    "axis1_algorithms",
    "axis2_algorithms",
    "axis1_parallel_programming",
    "axis2_parallel_programming",
    "axis1_math_for_computing",
    "axis2_math_for_computing",
    "axis1_linear_algebra",
    "axis2_linear_algebra",
    "axis1_calculus",
    "axis2_calculus",
    "axis1_probability_stats",
    "axis2_probability_stats",
    "skill_teamwork",
    "skill_ethics",
    "skill_communication",
    "skill_perseverance",
    "skill_discipline",
    "skill_collaboration",
    "skill_responsibility",
    "study_plan_comment",
    "time_total",
    "time_general_group",
    "time_feedback_group",
]

REQUIRED_COLUMNS = {"term", "year", "response_id"}

COLUMN_ALIASES = {
    "activities_influenced": ("activities_influenced", "activities_helped"),
    "impact_cc_industry_talk": ("impact_cc_industry_talk", "impact_cc_activity"),
    "impact_iti_industry_talk": ("impact_iti_industry_talk", "impact_iti_activity"),
    "impact_is_industry_talk": ("impact_is_industry_talk", "impact_is_activity"),
    "useful_student_roundtable": (
        "useful_student_roundtable",
        "useful_roundtable",
        "useful_graduate_roundtable",
    ),
    "useful_cc_industry_talk": ("useful_cc_industry_talk", "useful_cc_activity"),
    "useful_iti_industry_talk": ("useful_iti_industry_talk", "useful_iti_activity"),
    "useful_is_industry_talk": ("useful_is_industry_talk", "useful_is_activity"),
}


def _first_value(row: dict[str, str], columns: tuple[str, ...]) -> str:
    for column in columns:
        value = row.get(column, "")
        if value != "":
            return value
    return ""


def project_row(row: dict[str, str]) -> tuple[str, ...]:
    values = {column: row.get(column, "") for column in STAGING_COLUMNS}
    for target, aliases in COLUMN_ALIASES.items():
        values[target] = _first_value(row, aliases)
    return tuple(values[column] for column in STAGING_COLUMNS)


def iter_csv_rows(csv_path: Path) -> Iterator[tuple[str, ...]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise ValueError(f"Missing required CSV columns: {missing_text}")

        for row in reader:
            if None in row:
                raise ValueError(
                    f"CSV row {reader.line_num} has more values than the header"
                )
            yield project_row(row)


def _get_source_id(cursor) -> int:
    cursor.execute(
        "SELECT id_fuente FROM dw.dim_fuente_datos WHERE tipo = %s",
        (SOURCE_TYPE,),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError(f"Missing dw.dim_fuente_datos row for tipo={SOURCE_TYPE}")
    return row[0]


def run(config: EtlConfig) -> None:
    import psycopg

    csv_path = config.repo_root / SOURCE_FILE
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV source not found: {csv_path}")

    origin_file = csv_path.name
    target_columns = ["id_fuente", "archivo_origen", *STAGING_COLUMNS]
    copy_sql = f"""
        COPY {TARGET_TABLE} ({", ".join(target_columns)})
        FROM STDIN
    """

    inserted = 0
    with psycopg.connect(**config.connection_kwargs()) as conn:
        with conn.cursor() as cur:
            source_id = _get_source_id(cur)
            cur.execute(
                f"DELETE FROM {TARGET_TABLE} WHERE id_fuente = %s AND archivo_origen = %s",
                (source_id, origin_file),
            )
            with cur.copy(copy_sql) as copy:
                for row in iter_csv_rows(csv_path):
                    copy.write_row((source_id, origin_file, *row))
                    inserted += 1
        conn.commit()

    print(f"Loaded {inserted} rows from {SOURCE_FILE} into {TARGET_TABLE}")
