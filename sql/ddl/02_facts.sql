-- =============================================================
-- TABLAS DE HECHOS - Modelo estrella ECCI DW
-- =============================================================

-- -------------------------------------------------------------
-- FactRespuesta  (una fila por encuesta respondida)
-- -------------------------------------------------------------
CREATE TABLE dw.fact_respuesta (
    id_respuesta_sk     SERIAL PRIMARY KEY,
    id_respuesta_src    INTEGER     NOT NULL,  -- ID original del sistema fuente
    id_ciclo            INTEGER     NOT NULL REFERENCES dw.dim_ciclo(id_ciclo),
    id_tiempo_envio     INTEGER     REFERENCES dw.dim_tiempo(id_tiempo),
    id_tiempo_inicio    INTEGER     REFERENCES dw.dim_tiempo(id_tiempo),
    id_enfasis          INTEGER     REFERENCES dw.dim_enfasis(id_enfasis),
    id_semestre_decision INTEGER    REFERENCES dw.dim_semestre_carrera(id_semestre),
    id_fuente           INTEGER     NOT NULL REFERENCES dw.dim_fuente_datos(id_fuente),

    -- Asistencia y decisión
    asistio                 BOOLEAN,
    influyo_actividades     VARCHAR(20),  -- 'Sí', 'No', 'Parcialmente', 'N/A'
    razon_no_asistio        TEXT,
    razon_decision          TEXT,  -- '¿Cómo llegó a esa decisión?' (encuestas 2021/2022)
    comentario_poco_util    TEXT,
    comentario_le_gusto     TEXT,  -- 'liked_most'
    comentario_a_mejorar    TEXT,  -- 'liked_least_improve'
    comentario_general      TEXT,  -- 'study_plan_comment'

    -- Calidad de datos
    pagina_alcanzada        SMALLINT,  -- 'last_page': encuesta completa vs. abandonada
    idioma                  VARCHAR(5),

    -- Métricas de tiempo de respuesta (en segundos)
    tiempo_total_seg        NUMERIC(10,2),
    tiempo_info_general_seg NUMERIC(10,2),
    tiempo_retro_seg        NUMERIC(10,2),

    -- Metadatos ETL
    fecha_carga             TIMESTAMP NOT NULL DEFAULT NOW(),
    archivo_origen          VARCHAR(100)
);

CREATE INDEX idx_fact_respuesta_ciclo   ON dw.fact_respuesta(id_ciclo);
CREATE INDEX idx_fact_respuesta_enfasis ON dw.fact_respuesta(id_enfasis);
CREATE INDEX idx_fact_respuesta_fuente  ON dw.fact_respuesta(id_fuente);
CREATE UNIQUE INDEX idx_fact_respuesta_src ON dw.fact_respuesta(id_ciclo, id_respuesta_src);

-- -------------------------------------------------------------
-- FactCanalComunicacion  (qué canales usó cada respondente — N:M)
-- -------------------------------------------------------------
CREATE TABLE dw.fact_canal_comunicacion (
    id_respuesta_sk INTEGER NOT NULL REFERENCES dw.fact_respuesta(id_respuesta_sk),
    id_canal        INTEGER NOT NULL REFERENCES dw.dim_canal(id_canal),
    PRIMARY KEY (id_respuesta_sk, id_canal)
);

-- -------------------------------------------------------------
-- FactFactorDecision  (qué factores influyeron — N:M)
-- -------------------------------------------------------------
CREATE TABLE dw.fact_factor_decision (
    id_respuesta_sk INTEGER NOT NULL REFERENCES dw.fact_respuesta(id_respuesta_sk),
    id_factor       INTEGER NOT NULL REFERENCES dw.dim_factor_decision(id_factor),
    PRIMARY KEY (id_respuesta_sk, id_factor)
);

-- -------------------------------------------------------------
-- FactCalificacionActividad  (impacto y utilidad por actividad)
-- -------------------------------------------------------------
CREATE TABLE dw.fact_calificacion_actividad (
    id_respuesta_sk INTEGER     NOT NULL REFERENCES dw.fact_respuesta(id_respuesta_sk),
    id_actividad    INTEGER     NOT NULL REFERENCES dw.dim_actividad(id_actividad),
    impacto         SMALLINT    CHECK (impacto BETWEEN 1 AND 5),
    utilidad        SMALLINT    CHECK (utilidad BETWEEN 1 AND 5),
    PRIMARY KEY (id_respuesta_sk, id_actividad)
);

-- -------------------------------------------------------------
-- FactDificultadSemestre  (dificultad percibida por bloque de cursos)
-- -------------------------------------------------------------
CREATE TABLE dw.fact_dificultad_semestre (
    id_respuesta_sk INTEGER     NOT NULL REFERENCES dw.fact_respuesta(id_respuesta_sk),
    id_bloque       INTEGER     NOT NULL REFERENCES dw.dim_bloque_semestral(id_bloque),
    dificultad      SMALLINT    NOT NULL CHECK (dificultad BETWEEN 1 AND 5),
    PRIMARY KEY (id_respuesta_sk, id_bloque)
);

-- -------------------------------------------------------------
-- FactDominioConocimiento  (dominio propio + efectividad de enseñanza)
-- -------------------------------------------------------------
CREATE TABLE dw.fact_dominio_conocimiento (
    id_respuesta_sk     INTEGER     NOT NULL REFERENCES dw.fact_respuesta(id_respuesta_sk),
    id_area             INTEGER     NOT NULL REFERENCES dw.dim_area_conocimiento(id_area),
    dominio_propio      SMALLINT    CHECK (dominio_propio BETWEEN 1 AND 5),
    efectividad_ensenanza SMALLINT  CHECK (efectividad_ensenanza BETWEEN 1 AND 5),
    PRIMARY KEY (id_respuesta_sk, id_area)
);

-- -------------------------------------------------------------
-- FactHabilidadBlanda  (mejora en habilidades blandas)
-- -------------------------------------------------------------
CREATE TABLE dw.fact_habilidad_blanda (
    id_respuesta_sk INTEGER     NOT NULL REFERENCES dw.fact_respuesta(id_respuesta_sk),
    id_habilidad    INTEGER     NOT NULL REFERENCES dw.dim_habilidad_blanda(id_habilidad),
    mejora          SMALLINT    NOT NULL CHECK (mejora BETWEEN 1 AND 5),
    PRIMARY KEY (id_respuesta_sk, id_habilidad)
);

-- -------------------------------------------------------------
-- FactPerdidaCurso  (estudiantes que perdieron cursos por énfasis y ciclo — simulado)
-- -------------------------------------------------------------
CREATE TABLE dw.fact_perdida_curso (
    id_perdida      SERIAL PRIMARY KEY,
    id_ciclo        INTEGER     NOT NULL REFERENCES dw.dim_ciclo(id_ciclo),
    id_enfasis      INTEGER     NOT NULL REFERENCES dw.dim_enfasis(id_enfasis),
    matriculados    INTEGER     NOT NULL,
    reprobados      INTEGER     NOT NULL,
    tasa_reprobacion NUMERIC(5,2) GENERATED ALWAYS AS (
        CASE WHEN matriculados > 0 THEN (reprobados * 100.0 / matriculados) ELSE 0 END
    ) STORED,
    UNIQUE (id_ciclo, id_enfasis)
);

-- -------------------------------------------------------------
-- FactAuditoria  (log de cargas ETL)
-- -------------------------------------------------------------
CREATE TABLE dw.fact_auditoria (
    id_auditoria    SERIAL PRIMARY KEY,
    id_fuente       INTEGER     NOT NULL REFERENCES dw.dim_fuente_datos(id_fuente),
    id_ciclo        INTEGER     REFERENCES dw.dim_ciclo(id_ciclo),
    fecha_inicio    TIMESTAMP   NOT NULL,
    fecha_fin       TIMESTAMP,
    estado          VARCHAR(20) NOT NULL CHECK (estado IN ('EN_PROCESO', 'EXITOSO', 'FALLIDO')),
    registros_procesados INTEGER DEFAULT 0,
    registros_insertados INTEGER DEFAULT 0,
    registros_rechazados INTEGER DEFAULT 0,
    mensaje_error   TEXT
);
