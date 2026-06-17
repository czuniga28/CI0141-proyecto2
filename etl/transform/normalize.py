from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


# -------------------------------------------------------------------------
# Scalar value parsers
# -------------------------------------------------------------------------

_LIKERT_RE = re.compile(r"[1-5]")

# 3-level categorical impact (only present in the 2021/2022 surveys) mapped to
# the 1-5 ordinal scale stored in dw.fact_calificacion_actividad.impacto.
_IMPACTO_MAP = {
    "ningún impacto": 1,
    "ningun impacto": 1,
    "bajo impacto": 2,
    "alto impacto": 4,
}

_SI_VALUES = {"sí", "si", "yes", "true"}
_NO_VALUES = {"no", "false"}


def parse_likert(value: object) -> int | None:
    """Extract the 1-5 score embedded in a Likert answer.

    Handles every observed format ("3", "Muy fácil: 1", "Muy alto 5",
    "5 - Muy útil", "He mejorado mucho: 5"). Sentinels with no score
    ("No asistí", "M", "N/A", "", None) become ``None``.
    """

    if value is None:
        return None
    match = _LIKERT_RE.search(str(value))
    return int(match.group()) if match else None


def parse_impacto(value: object) -> int | None:
    """Map the categorical/numeric activity impact to a 1-5 ordinal."""

    if value is None:
        return None
    text = str(value).strip().lower()
    if not text:
        return None
    if text in _IMPACTO_MAP:
        return _IMPACTO_MAP[text]
    return parse_likert(text)


def parse_si_no(value: object) -> bool | None:
    """Map Sí/No answers to a boolean; anything else (N/A, blank) -> None."""

    if value is None:
        return None
    text = str(value).strip().lower()
    if text in _SI_VALUES:
        return True
    if text in _NO_VALUES:
        return False
    return None


def is_si(value: object) -> bool:
    """True only for an affirmative answer (for presence in bridge tables)."""

    return parse_si_no(value) is True


def parse_fecha(value: object) -> date | None:
    """Take the calendar date out of a timestamp string."""

    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        try:
            return datetime.strptime(text[:10], "%Y-%m-%d").date()
        except ValueError:
            return None


def parse_numeric(value: object) -> Decimal | None:
    """Parse a response-time (seconds) value into a Decimal."""

    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return None


def parse_int(value: object) -> int | None:
    """Parse a plain integer (e.g. last_page) tolerating blanks/decimals."""

    number = parse_numeric(value)
    return int(number) if number is not None else None


def clean_text(value: object) -> str | None:
    """Trim free-text, mapping blank/N/A to None."""

    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper() == "N/A":
        return None
    return text


def emphasis_code(value: object) -> str | None:
    """Extract the CC/IS/ITI code from 'CC: Ciencias de la Computación'."""

    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    code = text.split(":")[0].strip().upper()
    return code if code in {"CC", "IS", "ITI"} else None


_ROMAN_BY_TERM = {"i ciclo": "I", "ii ciclo": "II", "iii ciclo": "III"}


def ciclo_nombre(term: object, year: object) -> str | None:
    """Build the dim_ciclo natural key, e.g. ('I Ciclo', 2021) -> 'I-2021'."""

    if term is None or year is None:
        return None
    roman = _ROMAN_BY_TERM.get(str(term).strip().lower())
    year_text = str(year).strip()
    if roman is None or not year_text:
        return None
    return f"{roman}-{year_text}"


# -------------------------------------------------------------------------
# Source-column -> dimension natural-key mappings
# (target names match sql/ddl/03_seeds.sql exactly)
# -------------------------------------------------------------------------

HEARD_TO_CANAL = {
    "heard_email": "Correo institucional UCR",
    "heard_web": "Página web de la ECCI",
    "heard_social": "Redes sociales de la ECCI",
    "heard_element": "Plataforma Element",
    "heard_teachers": "Docentes",
    "heard_peers": "Compañeros o amigos",
    "heard_facebook": "Facebook de la ECCI",
    "heard_telegram": "Grupo de Telegram",
    "heard_other": "Otro",
}

# factor_other is free text; presence maps to 'Otro' (handled in load_facts).
FACTOR_TO_DIM = {
    "factor_professors": "Interacciones con profesores",
    "factor_courses": "Cursos que ha llevado hasta el momento",
    "factor_ecci_events": "Actividades organizadas por la ECCI",
    "factor_advanced_students": "Interacción con estudiantes avanzados en la carrera",
    "factor_study_plan": "Análisis del plan de estudios de cada énfasis",
    "factor_salary": "Expectativa de obtener un empleo bien remunerado",
    "factor_job_market": "Oferta de puestos disponibles en la industria",
}

FACTOR_OTHER_DIM = "Otro"

# suffix -> dim_area_conocimiento.nombre; axis1_<suffix>=dominio, axis2_<suffix>=enseñanza
AXIS_TO_AREA = {
    "programming": "Programación",
    "discrete_structures": "Estructuras discretas",
    "architecture": "Fundamentos de arquitectura",
    "assembly": "Lenguaje Ensamblador",
    "algorithms": "Análisis de algoritmos y estructuras de datos",
    "parallel_programming": "Programación paralela y concurrente",
    "math_for_computing": "Introducción a la matemática para computación",
    "linear_algebra": "Álgebra lineal",
    "calculus": "Cálculo diferencial e integral",
    "probability_stats": "Probabilidad y estadística",
}

SKILL_TO_HABILIDAD = {
    "skill_teamwork": "Capacidad de trabajar en equipos",
    "skill_ethics": "Actitud ética, con responsabilidad profesional y compromiso social",
    "skill_communication": "Comunicación asertiva",
    "skill_perseverance": "Perseverancia",
    "skill_discipline": "Disciplina",
    "skill_collaboration": "Colaboración",
    "skill_responsibility": "Responsabilidad",
}

# (useful_col, impact_col | None, dim_actividad.nombre). Names match 03_seeds.sql.
ACTIVITY_RATINGS = [
    ("useful_intro_talk", "impact_intro_talk", "Charla Introductoria de los Énfasis"),
    (
        "useful_student_roundtable",
        "impact_student_roundtable",
        "Mesa Redonda con los Estudiantes de los Énfasis",
    ),
    (
        "useful_admin_myths_talk",
        "impact_admin_myths_talk",
        "Charla Mitos y Realidades, y Proceso Administrativo",
    ),
    (
        "useful_admin_talk",
        None,
        "Charla informativa general sobre proceso administrativo",
    ),
    (
        "useful_cc_industry_talk",
        "impact_cc_industry_talk",
        "Charlas con Egresados-Industria: CC",
    ),
    (
        "useful_is_industry_talk",
        "impact_is_industry_talk",
        "Charlas con Egresados-Industria: IS",
    ),
    (
        "useful_iti_industry_talk",
        "impact_iti_industry_talk",
        "Charlas con Egresados-Industria: ITI",
    ),
    # Activities specific to the 2021/2022 surveys (no impact column).
    ("useful_cc_qa", None, "Q/A con estudiantes graduados"),
    ("useful_cc_fusion", None, "Computación Paralela y Energía de Fusión (CENAT)"),
    (
        "useful_is_inside",
        None,
        "IS desde adentro: plan de estudios con estudiantes avanzados",
    ),
    ("useful_is_google", None, "Software Engineering @ Google"),
    ("useful_iti_expectation", None, "Expectativa vs. Realidad: estudiantes avanzados"),
    (
        "useful_iti_security",
        None,
        "De la Bomba Binaria a la cacería de amenazas - Ciberseguridad",
    ),
    (
        "useful_iti_lora",
        None,
        "Arquitectura de red para agricultura de precisión (LoRa/WIFI/LTE)",
    ),
    ("useful_iti_jobs", None, "El entorno Laboral ITI: conversación con graduados"),
]

# difficulty_cycle_N -> dim_bloque_semestral.numero_ciclo
DIFFICULTY_TO_BLOQUE = {
    "difficulty_cycle_1": 1,
    "difficulty_cycle_2": 2,
    "difficulty_cycle_3": 3,
    "difficulty_cycle_4": 4,
}
