import unittest
from datetime import datetime, timezone
from forecast import upcoming_prices

class ForecastTests(unittest.TestCase):
    now = datetime(2026, 9, 1, 19, 10, tzinfo=timezone.utc)

    def test_future_window_preserves_negative_prices(self):
        data = [{"prices": [
            {"date_time": "2026-09-01T19:00:00Z", "agile_pred": -20},
            {"date_time": "2026-09-01T19:30:00.000Z", "agile_pred": -2.5},
            {"date_time": "2026-09-02T01:30:00Z", "agile_pred": -30}]}]
        rows = upcoming_prices(data, self.now)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], -2.5)

    def test_missing_data_fails(self):
        for data in ([], {}, [{"prices": []}], [{"prices": None}]):
            with self.assertRaises(ValueError):
                upcoming_prices(data, self.now)

    def test_invalid_value_fails(self):
        for value in (None, True, "0", float("nan")):
            with self.assertRaises(ValueError):
                upcoming_prices([{"prices": [{"date_time": "2026-09-01T19:30:00Z", "agile_pred": value}]}], self.now)

if __name__ == "__main__":
    unittest.main()
