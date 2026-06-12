-- =============================================================
-- STAGING - Zona de aterrizaje cruda
-- Refleja 1:1 el esquema fuente "encuesta_enfasis" (preprocessed_data/),
-- común a las 3 fuentes (CSV, BD relacional SQL Server, API/JSON).
-- Todo se carga como TEXT: la normalización ocurre en la capa Transform.
-- =============================================================

CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE staging.encuesta_enfasis_raw (
    id_staging              SERIAL PRIMARY KEY,
    id_fuente               INTEGER NOT NULL,  -- FK lógica a dw.dim_fuente_datos (sin constraint: staging es zona cruda)
    archivo_origen          VARCHAR(100),
    fecha_carga             TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Identificación
    term                    TEXT,
    year                    TEXT,
    response_id             TEXT,
    submitted_at            TEXT,
    started_at              TEXT,
    last_action_at          TEXT,
    last_page               TEXT,
    language                TEXT,
    seed                    TEXT,

    -- Canales por los que se enteró
    heard_email             TEXT,
    heard_web               TEXT,
    heard_social            TEXT,
    heard_element           TEXT,
    heard_teachers          TEXT,
    heard_peers             TEXT,
    heard_other             TEXT,
    heard_facebook          TEXT,  -- solo encuestas 2021/2022
    heard_telegram          TEXT,  -- solo encuestas 2021/2022

    -- Asistencia
    attended                TEXT,
    no_attendance_reason    TEXT,
    decision_semester       TEXT,
    activities_influenced   TEXT,  -- 'activities_helped' en encuestas viejas
    decision_reason         TEXT,

    -- Factores de decisión
    factor_professors           TEXT,
    factor_courses               TEXT,
    factor_ecci_events            TEXT,
    factor_advanced_students      TEXT,
    factor_study_plan             TEXT,
    factor_salary                 TEXT,
    factor_job_market              TEXT,
    factor_other                   TEXT,

    -- Impacto/utilidad de actividades (esquema 2023+)
    impact_intro_talk            TEXT,
    impact_student_roundtable    TEXT,
    impact_cc_industry_talk      TEXT,
    impact_iti_industry_talk     TEXT,
    impact_is_industry_talk      TEXT,
    impact_admin_myths_talk      TEXT,
    useful_intro_talk             TEXT,
    useful_student_roundtable     TEXT,
    useful_cc_industry_talk        TEXT,
    useful_iti_industry_talk       TEXT,
    useful_is_industry_talk        TEXT,
    useful_admin_myths_talk         TEXT,
    useful_admin_talk                TEXT,

    -- Utilidad de actividades (esquema 2021/2022)
    useful_cc_qa            TEXT,
    useful_cc_fusion        TEXT,
    useful_is_inside        TEXT,
    useful_is_google        TEXT,
    useful_iti_expectation  TEXT,
    useful_iti_security     TEXT,
    useful_iti_lora         TEXT,
    useful_iti_jobs         TEXT,

    low_usefulness_comment  TEXT,
    liked_most              TEXT,
    liked_least_improve     TEXT,

    -- Énfasis elegido
    chosen_emphasis         TEXT,

    -- Dificultad por bloque semestral (1-4)
    difficulty_cycle_1      TEXT,
    difficulty_cycle_2      TEXT,
    difficulty_cycle_3      TEXT,
    difficulty_cycle_4      TEXT,

    -- Dominio / efectividad de enseñanza por área (eje 1 = dominio, eje 2 = enseñanza)
    axis1_programming               TEXT,
    axis2_programming               TEXT,
    axis1_discrete_structures        TEXT,
    axis2_discrete_structures        TEXT,
    axis1_architecture                TEXT,
    axis2_architecture                TEXT,
    axis1_assembly                     TEXT,
    axis2_assembly                     TEXT,
    axis1_algorithms                    TEXT,
    axis2_algorithms                    TEXT,
    axis1_parallel_programming           TEXT,
    axis2_parallel_programming           TEXT,
    axis1_math_for_computing              TEXT,
    axis2_math_for_computing              TEXT,
    axis1_linear_algebra                   TEXT,
    axis2_linear_algebra                   TEXT,
    axis1_calculus                          TEXT,
    axis2_calculus                          TEXT,
    axis1_probability_stats                  TEXT,
    axis2_probability_stats                  TEXT,

    -- Habilidades blandas
    skill_teamwork          TEXT,
    skill_ethics            TEXT,
    skill_communication     TEXT,
    skill_perseverance      TEXT,
    skill_discipline        TEXT,
    skill_collaboration     TEXT,
    skill_responsibility    TEXT,
    study_plan_comment      TEXT,

    -- Tiempos de respuesta (segundos)
    time_total              TEXT,
    time_general_group      TEXT,
    time_feedback_group     TEXT
);

CREATE INDEX idx_staging_fuente ON staging.encuesta_enfasis_raw(id_fuente);
CREATE INDEX idx_staging_term_year ON staging.encuesta_enfasis_raw(term, year);
