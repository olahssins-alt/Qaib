import tempfile
import unittest
from datetime import date
from pathlib import Path

from teepublic_assistant import keywords as kw

SAMPLE_TRENDS = Path(__file__).parent.parent / "sample_data" / "sample_google_trends.csv"


class KeywordsTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.file = Path(self.dir.name) / "kw.csv"

    def tearDown(self):
        self.dir.cleanup()

    def test_numbers(self):
        self.assertEqual(kw._num("12,345"), 12345)
        self.assertEqual(kw._num("1.2k"), 1200)
        self.assertEqual(kw._num("<1"), 0.5)
        self.assertIsNone(kw._num(""))

    def test_init_refuses_to_overwrite(self):
        kw.init_file(self.file)
        with self.assertRaises(SystemExit):
            kw.init_file(self.file)

    def test_add_updates_existing_row(self):
        kw.init_file(self.file)
        kw.add_keywords(self.file, ["Pickleball Shirt"], teepublic="3,200")
        rows = kw.read_file(self.file)
        self.assertEqual(len(rows), 3)  # matched the starter row case-insensitively
        row = next(r for r in rows if r["keyword"].lower() == "pickleball shirt")
        self.assertEqual(row["teepublic_results"], "3,200")
        self.assertEqual(row["checked_on"], date.today().isoformat())

    def test_parse_google_trends_export(self):
        series = kw.parse_trends_csv(SAMPLE_TRENDS)
        self.assertEqual([s.keyword for s in series], ["pickleball shirt", "mahjong shirt", "nurse christmas shirt"])
        self.assertGreater(len(series[0].points), 100)
        self.assertEqual(series[2].peak_month(), "December")

    def test_parse_other_layouts(self):
        path = Path(self.dir.name) / "t.csv"
        path.write_text("Time,cat shirt\n\"Oct 5, 2025\",40\n\"Oct 12, 2025\",<1\n", encoding="utf-8")
        (s,) = kw.parse_trends_csv(path)
        self.assertEqual(s.points, [(date(2025, 10, 5), 40.0), (date(2025, 10, 12), 0.5)])
        path.write_text("Category: x\n\nnothing here\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            kw.parse_trends_csv(path)

    def test_import_and_score(self):
        kw.init_file(self.file)
        kw.add_keywords(self.file, ["mahjong shirt"], teepublic="640")
        kw.add_keywords(self.file, ["pickleball shirt"], teepublic="3200")
        kw.add_keywords(self.file, ["nurse christmas shirt"], teepublic="18500")
        kw.add_keywords(self.file, ["funny shirt"])
        kw.import_trends(self.file, SAMPLE_TRENDS)
        scored = kw.score_rows(kw.read_file(self.file), today=date(2026, 10, 6))
        self.assertEqual(scored[0]["keyword"], "mahjong shirt")
        self.assertTrue(scored[0]["verdict"].startswith("opportunity"))
        christmas = next(r for r in scored if r["keyword"] == "nurse christmas shirt")
        self.assertTrue(christmas["verdict"].startswith("seasonal"))
        self.assertIsNone(scored[-1]["score"])
        self.assertIn("needs", scored[-1]["verdict"])
        self.assertIn("mahjong shirt", kw.format_scores(scored))


if __name__ == "__main__":
    unittest.main()
