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
-- Áreas (id_area): 1=Programación, 2=Estructuras discretas, 3=Fund. arquitectura,
--   4=Lenguaje Ensamblador, 5=Análisis de algoritmos, 6=Prog. paralela,
--   7=Intro matemática para computación, 8=Álgebra lineal, 9=Cálculo, 10=Prob/Estadística
-- Tasas típicas simuladas:
--   Cálculo (~30-40%), Álgebra lineal (~25-35%), Prog. paralela (~25-32%)
--   Estructuras discretas (~22-28%), Algoritmos (~20-28%), Ensamblador (~18-25%)
--   Probabilidad (~18-25%), Fund. arquitectura (~15-22%), Programación (~12-18%)
--   Intro matemática (~10-15%)
INSERT INTO dw.fact_perdida_curso (id_ciclo, id_area, matriculados, reprobados) VALUES
    -- I-2021 (id_ciclo=1)
    (1, 1, 120, 16),
    (1, 2, 105, 26),
    (1, 3,  95, 16),
    (1, 4,  80, 17),
    (1, 5,  75, 18),
    (1, 6,  60, 17),
    (1, 7, 120, 13),
    (1, 8,  90, 25),
    (1, 9, 110, 37),
    (1, 10, 70, 14),
    -- II-2021 (id_ciclo=2)
    (2, 1, 115, 15),
    (2, 2, 100, 24),
    (2, 3,  90, 15),
    (2, 4,  78, 16),
    (2, 5,  72, 16),
    (2, 6,  58, 16),
    (2, 7, 115, 12),
    (2, 8,  88, 24),
    (2, 9, 105, 35),
    (2, 10, 68, 13),
    -- I-2022 (id_ciclo=3)
    (3, 1, 130, 18),
    (3, 2, 112, 28),
    (3, 3, 100, 18),
    (3, 4,  85, 19),
    (3, 5,  80, 20),
    (3, 6,  65, 19),
    (3, 7, 130, 15),
    (3, 8,  95, 28),
    (3, 9, 118, 42),
    (3, 10, 75, 16),
    -- II-2022 (id_ciclo=4)
    (4, 1, 125, 17),
    (4, 2, 108, 26),
    (4, 3,  96, 17),
    (4, 4,  82, 18),
    (4, 5,  77, 18),
    (4, 6,  62, 17),
    (4, 7, 125, 14),
    (4, 8,  92, 26),
    (4, 9, 112, 39),
    (4, 10, 72, 15),
    -- III-2022 (id_ciclo=5)
    (5, 1, 40, 5),
    (5, 2, 35, 8),
    (5, 3, 30, 5),
    (5, 4, 25, 5),
    (5, 5, 24, 6),
    (5, 6, 20, 6),
    (5, 7, 40, 4),
    (5, 8, 28, 8),
    (5, 9, 36, 13),
    (5, 10, 22, 4),
    -- I-2023 (id_ciclo=6)
    (6, 1, 135, 19),
    (6, 2, 115, 29),
    (6, 3, 102, 19),
    (6, 4,  88, 20),
    (6, 5,  82, 21),
    (6, 6,  68, 20),
    (6, 7, 135, 15),
    (6, 8,  98, 30),
    (6, 9, 122, 44),
    (6, 10, 78, 17),
    -- II-2023 (id_ciclo=7)
    (7, 1, 128, 17),
    (7, 2, 110, 27),
    (7, 3,  97, 16),
    (7, 4,  84, 18),
    (7, 5,  78, 18),
    (7, 6,  64, 18),
    (7, 7, 128, 14),
    (7, 8,  93, 27),
    (7, 9, 115, 40),
    (7, 10, 74, 15),
    -- I-2024 (id_ciclo=8)
    (8, 1, 140, 20),
    (8, 2, 120, 31),
    (8, 3, 105, 20),
    (8, 4,  90, 21),
    (8, 5,  85, 22),
    (8, 6,  72, 22),
    (8, 7, 140, 16),
    (8, 8, 100, 31),
    (8, 9, 126, 47),
    (8, 10, 80, 18),
    -- II-2024 (id_ciclo=9)
    (9, 1, 132, 18),
    (9, 2, 114, 28),
    (9, 3, 100, 18),
    (9, 4,  86, 19),
    (9, 5,  80, 19),
    (9, 6,  68, 19),
    (9, 7, 132, 14),
    (9, 8,  95, 28),
    (9, 9, 120, 42),
    (9, 10, 76, 16),
    -- I-2025 (id_ciclo=10)
    (10, 1, 145, 21),
    (10, 2, 125, 33),
    (10, 3, 108, 21),
    (10, 4,  92, 22),
    (10, 5,  88, 23),
    (10, 6,  75, 23),
    (10, 7, 145, 17),
    (10, 8, 103, 33),
    (10, 9, 130, 49),
    (10, 10, 82, 19),
    -- II-2025 (id_ciclo=11)
    (11, 1, 138, 19),
    (11, 2, 118, 29),
    (11, 3, 102, 18),
    (11, 4,  88, 20),
    (11, 5,  82, 20),
    (11, 6,  70, 20),
    (11, 7, 138, 15),
    (11, 8,  98, 29),
    (11, 9, 124, 44),
    (11, 10, 78, 17);
