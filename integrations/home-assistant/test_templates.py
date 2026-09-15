"""Fixture tests for Jinja expressions, not a running Home Assistant instance."""
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
import yaml
from jinja2 import Environment, StrictUndefined


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.config = yaml.safe_load(
            Path(__file__).with_name("agile_forecast.yaml").read_text()
        )
        self.now = datetime(2026, 9, 1, 19, 10, tzinfo=timezone.utc)
        self.rows = [
            dict(date_time="2026-09-01T19:00:00Z", agile_pred=12, agile_high=15, price=12),
            dict(date_time="2026-09-01T19:30:00.000Z", agile_pred=-2, agile_high=3, price=-2),
        ]
        self.fetched = self.now
        self.env = Environment(undefined=StrictUndefined)

        def timestamp(value, default=None):
            try:
                if isinstance(value, str):
                    value = datetime.fromisoformat(value.replace("Z", "+00:00"))
                return value.timestamp()
            except (TypeError, ValueError, AttributeError):
                return default

        self.env.globals.update(
            now=lambda: self.now,
            utcnow=lambda: self.now,
            as_timestamp=timestamp,
            state_attr=lambda entity, attr: self.rows,
            states=lambda entity: self.fetched.isoformat(),
            has_value=lambda entity: True,
        )

    def render(self, sensor, key="state"):
        return self.env.from_string(sensor[key]).render().strip()

    def test_current_prices_and_negative_future_minimum(self):
        sensors = self.config["template"][0]["sensor"]
        self.assertEqual([float(self.render(s)) for s in sensors], [12, 15, -2, 12])
        self.assertTrue(all(self.render(s, "availability") == "True" for s in sensors))

    def test_future_is_not_current(self):
        self.rows = self.rows[1:]
        sensors = self.config["template"][0]["sensor"]
        for index in (0, 1, 3):
            self.assertEqual(self.render(sensors[index]), "None")
        self.assertEqual(float(self.render(sensors[2])), -2)

    def test_empty_data_is_not_zero(self):
        self.rows = []
        for sensor in self.config["template"][0]["sensor"]:
            self.assertEqual(self.render(sensor), "None")

    def test_stale_data_unavailable(self):
        self.fetched = self.now - timedelta(hours=3)
        for sensor in self.config["template"][0]["sensor"]:
            self.assertEqual(self.render(sensor, "availability"), "False")

    def test_boundary_advances_current_slot(self):
        self.now = self.now.replace(minute=30)
        sensors = self.config["template"][0]["sensor"]
        self.assertEqual(float(self.render(sensors[0])), -2)
        self.assertEqual(float(self.render(sensors[3])), -2)


if __name__ == "__main__":
    unittest.main()