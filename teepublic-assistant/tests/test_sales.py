import io
import tempfile
import unittest
from datetime import date
from pathlib import Path

from teepublic_assistant import sales
from teepublic_assistant.cli import main


def write_csv(text: str) -> str:
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    return f.name


class ParseTests(unittest.TestCase):
    def test_money(self):
        self.assertEqual(sales.parse_money("$1,234.50"), 1234.5)
        self.assertEqual(sales.parse_money("(3.20)"), -3.2)
        self.assertEqual(sales.parse_money("-$2"), -2.0)
        self.assertEqual(sales.parse_money(""), 0.0)

    def test_dates(self):
        self.assertEqual(sales.parse_date("09/30/2026"), date(2026, 9, 30))
        self.assertEqual(sales.parse_date("2026-09-30"), date(2026, 9, 30))
        self.assertEqual(sales.parse_date("Sep 30, 2026"), date(2026, 9, 30))
        self.assertIsNone(sales.parse_date("not a date"))

    def test_aliases_and_overrides(self):
        cols = sales.resolve_columns(["Sale Date", "Design Title", "Product Type", "Royalty"])
        self.assertEqual(cols["date"], "Sale Date")
        self.assertEqual(cols["design"], "Design Title")
        self.assertEqual(cols["product"], "Product Type")
        self.assertEqual(cols["earnings"], "Royalty")
        cols = sales.resolve_columns(["When", "Thing", "Money"], {"design": "Thing", "earnings": "Money"})
        self.assertEqual(cols["design"], "Thing")
        with self.assertRaises(ValueError):
            sales.resolve_columns(["When", "Money"])


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.path = write_csv(
            "Date,Design,Product,Retail Price,Earnings,Status\n"
            "01/05/2026,Retro Cat,T-Shirt,$24.00,$4.00,Completed\n"
            "01/06/2026,Retro Cat,Sticker,$4.00,$0.60,Completed\n"
            "02/01/2026,Retro Cat,T-Shirt,$24.00,-$4.00,Refunded\n"
            "02/02/2026,Plant Mom,Mug,$16.00,$2.00,Completed\n"
        )

    def tearDown(self):
        Path(self.path).unlink()

    def test_summary(self):
        s = sales.summarize(sales.load_sales(self.path))
        self.assertEqual(s["totals"]["orders"], 3)
        self.assertEqual(s["totals"]["refunds"], 1)
        self.assertAlmostEqual(s["totals"]["earnings"], 2.60)
        self.assertEqual(s["top_designs"][0]["design"], "Plant Mom")
        self.assertEqual(s["by_product_type"][0]["product"], "Mug")
        self.assertEqual([m["month"] for m in s["monthly"]], ["2026-01", "2026-02"])
        self.assertEqual(s["period"], {"start": "2026-01-05", "end": "2026-02-02"})

    def test_report_command(self):
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main(["report", self.path])
        self.assertIn("TEEPUBLIC SALES REPORT", buf.getvalue())
        self.assertIn("Retro Cat", buf.getvalue())


class SampleDataTest(unittest.TestCase):
    def test_sample_loads(self):
        path = Path(__file__).parent.parent / "sample_data" / "sample_sales.csv"
        s = sales.summarize(sales.load_sales(path))
        self.assertGreater(s["totals"]["orders"], 100)
        self.assertIsNotNone(s["momentum"])


if __name__ == "__main__":
    unittest.main()
