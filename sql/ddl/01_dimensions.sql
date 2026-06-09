-- =============================================================
-- DIMENSIONES - Modelo estrella ECCI DW
-- Cliente: Escuela de Ciencias de la Computación e Informática (ECCI-UCR)
-- Dominio: Encuestas de ingreso a énfasis (2021-2025)
-- =============================================================

CREATE SCHEMA IF NOT EXISTS dw;

-- -------------------------------------------------------------
-- DimTiempo
-- -------------------------------------------------------------
CREATE TABLE dw.dim_tiempo (
    id_tiempo       SERIAL PRIMARY KEY,
    fecha           DATE        NOT NULL UNIQUE,
    año             SMALLINT    NOT NULL,
    mes             SMALLINT    NOT NULL,
    dia             SMALLINT    NOT NULL,
    dia_semana      VARCHAR(10) NOT NULL,  -- Lunes, Martes, ...
    trimestre       SMALLINT    NOT NULL   -- 1-4
);

-- -------------------------------------------------------------
-- DimCiclo  (I-2021, II-2021, ..., II-2025)
-- -------------------------------------------------------------
CREATE TABLE dw.dim_ciclo (
    id_ciclo        SERIAL PRIMARY KEY,
    ciclo_nombre    VARCHAR(20) NOT NULL UNIQUE,  -- 'I-2021'
    año             SMALLINT    NOT NULL,
    numero_ciclo    VARCHAR(5)  NOT NULL           -- 'I', 'II', 'III'
);

-- -------------------------------------------------------------
-- DimEnfasis  (CC, IS, ITI)
-- -------------------------------------------------------------
CREATE TABLE dw.dim_enfasis (
    id_enfasis      SERIAL PRIMARY KEY,
    codigo          VARCHAR(5)  NOT NULL UNIQUE,  -- 'CC', 'IS', 'ITI'
    nombre          VARCHAR(80) NOT NULL
);

-- -------------------------------------------------------------
-- DimSemestreCarrera  (en qué semestre tomó la decisión)
-- -------------------------------------------------------------
CREATE TABLE dw.dim_semestre_carrera (
    id_semestre     SERIAL PRIMARY KEY,
    descripcion     VARCHAR(60) NOT NULL UNIQUE   -- 'I ciclo 1er año', etc.
);

-- -------------------------------------------------------------
-- DimCanal  (cómo se enteró de las actividades)
-- -------------------------------------------------------------
CREATE TABLE dw.dim_canal (
    id_canal        SERIAL PRIMARY KEY,
    nombre          VARCHAR(60) NOT NULL UNIQUE
    -- 'Correo institucional UCR', 'Página web de la ECCI',
    -- 'Redes sociales de la ECCI', 'Plataforma Element',
    -- 'Docentes', 'Compañeros o amigos', 'Otro'
);

-- -------------------------------------------------------------
-- DimFactorDecision  (factores que influyeron en la elección)
-- -------------------------------------------------------------
CREATE TABLE dw.dim_factor_decision (
    id_factor       SERIAL PRIMARY KEY,
    nombre          VARCHAR(120) NOT NULL UNIQUE
    -- 'Interacciones con profesores', 'Cursos que ha llevado',
    -- 'Actividades organizadas por la ECCI', etc.
);

-- -------------------------------------------------------------
-- DimActividad  (charlas y actividades de énfasis)
-- -------------------------------------------------------------
CREATE TABLE dw.dim_actividad (
    id_actividad    SERIAL PRIMARY KEY,
    nombre          VARCHAR(150) NOT NULL UNIQUE,
    enfasis_codigo  VARCHAR(5)   -- NULL = aplica a todos; 'CC', 'IS', 'ITI'
);

-- -------------------------------------------------------------
-- DimBloqueSemestral  (bloques de cursos por ciclo para calificar dificultad)
-- -------------------------------------------------------------
CREATE TABLE dw.dim_bloque_semestral (
    id_bloque       SERIAL PRIMARY KEY,
    numero_ciclo    SMALLINT    NOT NULL,  -- 1, 2, 3, 4
    descripcion     TEXT        NOT NULL   -- lista de cursos del bloque
);

-- -------------------------------------------------------------
-- DimAreaConocimiento  (áreas para calificar dominio y enseñanza)
-- -------------------------------------------------------------
CREATE TABLE dw.dim_area_conocimiento (
    id_area         SERIAL PRIMARY KEY,
    nombre          VARCHAR(80) NOT NULL UNIQUE
    -- 'Programación', 'Estructuras discretas', 'Fundamentos de arquitectura', ...
);

-- -------------------------------------------------------------
-- DimHabilidadBlanda
-- -------------------------------------------------------------
CREATE TABLE dw.dim_habilidad_blanda (
    id_habilidad    SERIAL PRIMARY KEY,
    nombre          VARCHAR(80) NOT NULL UNIQUE
    -- 'Capacidad de trabajar en equipos', 'Actitud ética', ...
);

-- -------------------------------------------------------------
-- DimFuenteDatos  (trazabilidad ETL: CSV / BD relacional / API)
-- -------------------------------------------------------------
CREATE TABLE dw.dim_fuente_datos (
    id_fuente       SERIAL PRIMARY KEY,
    tipo            VARCHAR(20) NOT NULL UNIQUE,  -- 'CSV', 'BD_RELACIONAL', 'API'
    descripcion     VARCHAR(120)
);
