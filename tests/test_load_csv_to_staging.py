import unittest
from pathlib import Path

from etl.load_csv_to_staging import SOURCE_COLUMNS, iter_csv_rows, project_row


class LoadCsvToStagingTests(unittest.TestCase):
    def test_projects_historical_column_names(self):
        row = {
            "term": "I Ciclo",
            "year": "2021",
            "response_id": "42",
            "activities_helped": "Si",
            "impact_cc_activity": "5 - Muy util",
            "useful_roundtable": "4",
        }

        projected = dict(zip(SOURCE_COLUMNS, project_row(row), strict=True))

        self.assertEqual(projected["activities_influenced"], "Si")
        self.assertEqual(projected["impact_cc_industry_talk"], "5 - Muy util")
        self.assertEqual(projected["useful_student_roundtable"], "4")
        self.assertEqual(projected["heard_facebook"], "")

    def test_reads_all_rows_from_the_project_csv(self):
        repo_root = Path(__file__).resolve().parents[1]
        csv_path = repo_root / "preprocessed_data" / "encuesta_enfasis.csv"

        rows = list(iter_csv_rows(csv_path))

        self.assertEqual(len(rows), 269)
        self.assertTrue(all(len(row) == len(SOURCE_COLUMNS) for row in rows))


if __name__ == "__main__":
    unittest.main()
