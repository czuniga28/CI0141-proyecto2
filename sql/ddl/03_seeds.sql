-- =============================================================
-- DATOS SEMILLA - Valores conocidos de las dimensiones
-- =============================================================

-- DimFuenteDatos
INSERT INTO dw.dim_fuente_datos (tipo, descripcion) VALUES
    ('CSV',          'Archivos Excel/CSV exportados por ciclo'),
    ('BD_RELACIONAL','Base de datos PostgreSQL relacional (fuente secundaria)'),
    ('API',          'API REST mock que sirve los datos en formato JSON');

-- DimEnfasis
INSERT INTO dw.dim_enfasis (codigo, nombre) VALUES
    ('CC',  'Ciencias de la Computación'),
    ('IS',  'Ingeniería de Software'),
    ('ITI', 'Ingeniería de Tecnologías de la Información');

-- DimCiclo
INSERT INTO dw.dim_ciclo (ciclo_nombre, año, numero_ciclo) VALUES
    ('I-2021',   2021, 'I'),
    ('II-2021',  2021, 'II'),
    ('I-2022',   2022, 'I'),
    ('II-2022',  2022, 'II'),
    ('III-2022', 2022, 'III'),
    ('I-2023',   2023, 'I'),
    ('II-2023',  2023, 'II'),
    ('I-2024',   2024, 'I'),
    ('II-2024',  2024, 'II'),
    ('I-2025',   2025, 'I'),
    ('II-2025',  2025, 'II');

-- DimCanal
INSERT INTO dw.dim_canal (nombre) VALUES
    ('Correo institucional UCR'),
    ('Página web de la ECCI'),
    ('Redes sociales de la ECCI'),
    ('Plataforma Element'),
    ('Docentes'),
    ('Compañeros o amigos'),
    ('Facebook de la ECCI'),
    ('Grupo de Telegram'),
    ('Otro');

-- DimFactorDecision
INSERT INTO dw.dim_factor_decision (nombre) VALUES
    ('Interacciones con profesores'),
    ('Cursos que ha llevado hasta el momento'),
    ('Actividades organizadas por la ECCI'),
    ('Interacción con estudiantes avanzados en la carrera'),
    ('Análisis del plan de estudios de cada énfasis'),
    ('Expectativa de obtener un empleo bien remunerado'),
    ('Oferta de puestos disponibles en la industria'),
    ('Otro');

-- DimActividad
INSERT INTO dw.dim_actividad (nombre, enfasis_codigo) VALUES
    ('Charla Introductoria de los Énfasis',                         NULL),
    ('Mesa Redonda con los Estudiantes de los Énfasis',             NULL),
    ('Charla Mitos y Realidades, y Proceso Administrativo',         NULL),
    ('Charla informativa general sobre proceso administrativo',     NULL),
    ('Q/A con estudiantes graduados',                               'CC'),
    ('Computación Paralela y Energía de Fusión (CENAT)',            'CC'),
    ('IS desde adentro: plan de estudios con estudiantes avanzados','IS'),
    ('Software Engineering @ Google',                               'IS'),
    ('Expectativa vs. Realidad: estudiantes avanzados',             'ITI'),
    ('De la Bomba Binaria a la cacería de amenazas - Ciberseguridad','ITI'),
    ('Arquitectura de red para agricultura de precisión (LoRa/WIFI/LTE)', 'ITI'),
    ('El entorno Laboral ITI: conversación con graduados',          'ITI'),
    ('Charlas con Egresados-Industria: CC',                         'CC'),
    ('Charlas con Egresados-Industria: IS',                         'IS'),
    ('Charlas con Egresados-Industria: ITI',                        'ITI');

-- DimBloqueSemestral
INSERT INTO dw.dim_bloque_semestral (numero_ciclo, descripcion) VALUES
    (1, 'I ciclo: Introducción a la Computación + Introducción a la Matemática + Generales + Inglés + Deportiva'),
    (2, 'II ciclo: Estructuras Discretas + Programación 1 + Cálculo 1 + Generales'),
    (3, 'III ciclo: Programación 2 + Fundamentos de Arquitectura + Cálculo 2 + Álgebra Lineal + Seminario de Realidad Nacional'),
    (4, 'IV ciclo: Programación Paralela y Concurrente + Análisis de Algoritmos + Probabilidad y Estadística + Lenguaje Ensamblador + Proyecto Integrador');

-- DimAreaConocimiento
INSERT INTO dw.dim_area_conocimiento (nombre) VALUES
    ('Programación'),
    ('Estructuras discretas'),
    ('Fundamentos de arquitectura'),
    ('Lenguaje Ensamblador'),
    ('Análisis de algoritmos y estructuras de datos'),
    ('Programación paralela y concurrente'),
    ('Introducción a la matemática para computación'),
    ('Álgebra lineal'),
    ('Cálculo diferencial e integral'),
    ('Probabilidad y estadística');

-- DimHabilidadBlanda
INSERT INTO dw.dim_habilidad_blanda (nombre) VALUES
    ('Capacidad de trabajar en equipos'),
    ('Actitud ética, con responsabilidad profesional y compromiso social'),
    ('Comunicación asertiva'),
    ('Perseverancia'),
    ('Disciplina'),
    ('Colaboración'),
    ('Responsabilidad');

-- DimSemestreCarrera (valores conocidos de los datos)
INSERT INTO dw.dim_semestre_carrera (descripcion) VALUES
    ('I semestre del 1er año'),
    ('II semestre del 1er año'),
    ('I semestre del 2do año'),
    ('II semestre del 2do año'),
    ('I semestre del 3er año'),
    ('II semestre del 3er año'),
    ('Otro');

-- FactPerdidaCurso (datos simulados para proyección de demanda)
-- CC (id_enfasis=1): tasa ~25-35% (cursos teóricos/matemáticos más exigentes)
-- IS (id_enfasis=2): tasa ~18-25%
-- ITI (id_enfasis=3): tasa ~15-22%
INSERT INTO dw.fact_perdida_curso (id_ciclo, id_enfasis, matriculados, reprobados) VALUES
    -- I-2021  (id_ciclo=1)
    (1, 1, 38, 11),
    (1, 2, 45, 9),
    (1, 3, 37, 6),
    -- II-2021 (id_ciclo=2)
    (2, 1, 35, 10),
    (2, 2, 42, 8),
    (2, 3, 38, 7),
    -- I-2022  (id_ciclo=3)
    (3, 1, 40, 13),
    (3, 2, 50, 11),
    (3, 3, 40, 7),
    -- II-2022 (id_ciclo=4)
    (4, 1, 37, 11),
    (4, 2, 48, 10),
    (4, 3, 40, 8),
    -- III-2022 (id_ciclo=5)
    (5, 1, 12, 4),
    (5, 2, 15, 3),
    (5, 3, 13, 2),
    -- I-2023  (id_ciclo=6)
    (6, 1, 42, 14),
    (6, 2, 52, 12),
    (6, 3, 41, 7),
    -- II-2023 (id_ciclo=7)
    (7, 1, 39, 11),
    (7, 2, 49, 10),
    (7, 3, 40, 7),
    -- I-2024  (id_ciclo=8)
    (8, 1, 44, 15),
    (8, 2, 55, 13),
    (8, 3, 41, 8),
    -- II-2024 (id_ciclo=9)
    (9, 1, 40, 12),
    (9, 2, 52, 11),
    (9, 3, 40, 7),
    -- I-2025  (id_ciclo=10)
    (10, 1, 46, 15),
    (10, 2, 57, 13),
    (10, 3, 42, 8),
    -- II-2025 (id_ciclo=11)
    (11, 1, 42, 12),
    (11, 2, 54, 11),
    (11, 3, 42, 7);
