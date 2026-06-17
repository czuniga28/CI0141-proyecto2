import unittest
from datetime import date
from decimal import Decimal

from etl.transform import normalize as nz


class ParseLikertTests(unittest.TestCase):
    def test_extracts_score_from_every_observed_format(self):
        cases = {
            "3": 3,
            "Muy fácil: 1": 1,
            "Muy difícil: 5": 5,
            "Muy alto 5": 5,
            "Muy bajo 1": 1,
            "He mejorado mucho: 5": 5,
            "No he mejorado: 1": 1,
            "5 - Muy útil": 5,
            "1 - Nada útil": 1,
        }
        for raw, expected in cases.items():
            self.assertEqual(nz.parse_likert(raw), expected, raw)

    def test_sentinels_and_blanks_become_none(self):
        for raw in ("No asistí", "M", "N/A", "", None):
            self.assertIsNone(nz.parse_likert(raw), raw)


class ParseImpactoTests(unittest.TestCase):
    def test_maps_categorical_levels(self):
        self.assertEqual(nz.parse_impacto("Ningún impacto"), 1)
        self.assertEqual(nz.parse_impacto("Bajo impacto"), 2)
        self.assertEqual(nz.parse_impacto("Alto impacto"), 4)

    def test_no_asistio_and_blank_are_none(self):
        self.assertIsNone(nz.parse_impacto("No asistí"))
        self.assertIsNone(nz.parse_impacto(""))
        self.assertIsNone(nz.parse_impacto(None))

    def test_numeric_fallback(self):
        self.assertEqual(nz.parse_impacto("4"), 4)


class ParseSiNoTests(unittest.TestCase):
    def test_affirmative_and_negative(self):
        self.assertIs(nz.parse_si_no("Sí"), True)
        self.assertIs(nz.parse_si_no("si"), True)
        self.assertIs(nz.parse_si_no("No"), False)

    def test_other_values_are_none(self):
        for raw in ("N/A", "", None, "Parcialmente"):
            self.assertIsNone(nz.parse_si_no(raw), raw)

    def test_is_si_helper(self):
        self.assertTrue(nz.is_si("Sí"))
        self.assertFalse(nz.is_si("No"))
        self.assertFalse(nz.is_si(None))


class EmphasisAndCicloTests(unittest.TestCase):
    def test_emphasis_code(self):
        self.assertEqual(nz.emphasis_code("CC: Ciencias de la Computación"), "CC")
        self.assertEqual(nz.emphasis_code("IS: Ingeniería de Software"), "IS")
        self.assertEqual(
            nz.emphasis_code("ITI: Ingeniería de Tecnologías de la Información"), "ITI"
        )
        self.assertIsNone(nz.emphasis_code(""))
        self.assertIsNone(nz.emphasis_code(None))

    def test_ciclo_nombre(self):
        self.assertEqual(nz.ciclo_nombre("I Ciclo", 2021), "I-2021")
        self.assertEqual(nz.ciclo_nombre("II Ciclo", "2022"), "II-2022")
        self.assertEqual(nz.ciclo_nombre("III Ciclo", 2022), "III-2022")
        self.assertIsNone(nz.ciclo_nombre(None, 2021))
        self.assertIsNone(nz.ciclo_nombre("X Ciclo", 2021))


class ParsePrimitivesTests(unittest.TestCase):
    def test_parse_fecha(self):
        self.assertEqual(nz.parse_fecha("2021-05-20 20:19:58"), date(2021, 5, 20))
        self.assertEqual(nz.parse_fecha("2025-05-14"), date(2025, 5, 14))
        self.assertIsNone(nz.parse_fecha(""))
        self.assertIsNone(nz.parse_fecha(None))

    def test_parse_numeric(self):
        self.assertEqual(nz.parse_numeric("1868.04"), Decimal("1868.04"))
        self.assertIsNone(nz.parse_numeric(""))
        self.assertIsNone(nz.parse_numeric("n/d"))

    def test_parse_int(self):
        self.assertEqual(nz.parse_int("2"), 2)
        self.assertEqual(nz.parse_int("2.0"), 2)
        self.assertIsNone(nz.parse_int(""))

    def test_clean_text(self):
        self.assertEqual(nz.clean_text("  hola  "), "hola")
        self.assertIsNone(nz.clean_text("N/A"))
        self.assertIsNone(nz.clean_text(""))
        self.assertIsNone(nz.clean_text(None))


if __name__ == "__main__":
    unittest.main()
