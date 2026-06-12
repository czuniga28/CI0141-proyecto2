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
