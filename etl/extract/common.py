"""Shared constants and helpers for extract modules.

All sources land in the same raw staging table, columns shared with the
"encuesta_enfasis" schema (preprocessed_data/) common to the 3 sources
(CSV, relational mock DB, JSON/API mock).
"""

from __future__ import annotations


TARGET_TABLE = "staging.encuesta_enfasis_raw"

SOURCE_COLUMNS = [
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
    "attended",
    "no_attendance_reason",
    "decision_semester",
    "activities_influenced",
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
    "low_usefulness_comment",
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


def get_source_id(cursor, source_type: str) -> int:
    """Look up the dw.dim_fuente_datos surrogate key for a source type."""

    cursor.execute(
        "SELECT id_fuente FROM dw.dim_fuente_datos WHERE tipo = %s",
        (source_type,),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError(f"Missing dw.dim_fuente_datos row for tipo={source_type}")
    return row[0]
