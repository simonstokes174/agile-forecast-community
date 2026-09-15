#!/usr/bin/env python3
"""Fetch a forecast without dependencies. Missing values never become free energy."""
import argparse
import json
import math
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen

REGIONS = set("ABCDEFGHJKLMNPX")

def upcoming_prices(payload, now):
    if not isinstance(payload, list) or not payload or not isinstance(payload[0], dict):
        raise ValueError("Expected a non-empty forecast response array")
    prices = payload[0].get("prices")
    if not isinstance(prices, list):
        raise ValueError("Missing prices array")
    result = []
    for row in prices:
        if not isinstance(row, dict):
            raise ValueError("Malformed price row")
        dt = datetime.fromisoformat(row["date_time"].replace("Z", "+00:00"))
        value = row["agile_pred"]
        if dt.tzinfo is None or isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("Invalid timestamp or price")
        if now <= dt < now + timedelta(hours=6):
            result.append((dt, value))
    if not result:
        raise ValueError("No usable future slots in the next six hours")
    return sorted(result)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", default="C", choices=sorted(REGIONS))
    args = parser.parse_args()
    request = Request("https://agileforecast.co.uk/api/" + args.region + "/?hours=24", headers={"User-Agent": "agile-forecast-community-example/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            if response.status != 200:
                raise ValueError("Forecast not ready: HTTP " + str(response.status))
            payload = json.load(response)
        now = datetime.now(timezone.utc)
        rows = upcoming_prices(payload, now)
        dt, value = min(rows, key=lambda row: row[1])
        print("Cheapest future half-hour in next 6h:", dt.isoformat(), f"{value:.2f} p/kWh")
        print("Forecast vintage:", payload[0].get("created_at", "not supplied"))
        print("This is a forecast endpoint; confirm the published rate before acting.")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, "Unable to obtain usable prices: " + str(exc) + "\n")

if __name__ == "__main__":
    main()
