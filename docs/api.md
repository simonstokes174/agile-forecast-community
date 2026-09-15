# Public API guide

Base URL: https://agileforecast.co.uk/api

These public endpoints currently require no API key. Use HTTPS. Cache responses, avoid parallel polling for the same region, and back off on errors. Suggested intervals below are client guidance, not a guaranteed service limit or SLA.

## Regions

GET /regions returns objects with code and name. Use your electricity supply region, not simply a nearby city. X is the national average and is not your household tariff.

| Code | Region |
|---|---|
| A | Eastern England |
| B | East Midlands |
| C | London |
| D | Merseyside and Northern Wales |
| E | West Midlands |
| F | North Eastern England |
| G | North Western England |
| H | Southern England |
| J | South Eastern England |
| K | Southern Wales |
| L | South Western England |
| M | Yorkshire |
| N | Southern Scotland |
| P | Northern Scotland |
| X | National Average |

## Forecast

GET /C/ returns an array whose first object contains name, created_at, and prices. Each price row contains:

| Field | Meaning |
|---|---|
| date_time | ISO 8601 timestamp for the start of a half-hour slot |
| agile_pred | Central price in pence per kWh |
| agile_low / agile_high | Estimated lower/upper price band; not a guaranteed bound or fixed confidence level |
| is_published | Whether this row uses a published rate rather than a prediction |

Example shape (illustrative values, not current prices):

```json
[{"name":"Region | C …","created_at":"2026-09-01T06:00:00Z","prices":[{"date_time":"2026-09-03T12:00:00Z","agile_pred":18.2,"agile_low":12.0,"agile_high":24.4,"is_published":false}]}]
```

The maximum forecast horizon is currently 21 days. A response can be shorter as a stored forecast ages. Optional query parameters:

- days=1..21: up to N × 48 half-hour rows; these are not London calendar-day boundaries.
- hours=1..504: up to N × 2 rows. days takes precedence if both are supplied.
- high_low=false: returns date_time and agile_pred only, omitting bands and is_published. Do not use this when you need publication attribution.

Example: https://agileforecast.co.uk/api/C/?hours=24

Poll roughly every 30 minutes for planning. The API may serve cached data; created_at is the forecast vintage, not the request time. HTTP 202 with an empty prices array can mean generation is pending. Retry later with backoff; do not replace it with a free-energy value.

## Confirmed rates

GET /C/confirmed returns an object with confirmed_rates, fetched_at, and count. Rows contain date_time and price (pence per kWh). These are published Octopus rates, available only through the latest published delivery period, not the entire forecast horizon.

```json
{"confirmed_rates":[{"date_time":"2026-09-01T12:00:00Z","price":18.2}],"fetched_at":"2026-09-01T12:10:00Z","count":1}
```

Rows may be newest-first and can include recent past slots. Never assume the first row is current. A 200 response can contain an empty array during an upstream failure. Suggested polling interval: 10 minutes.

## Time and units

- Parse timestamps as timezone-aware instants. The Z suffix means UTC; fractional seconds may be present or absent.
- A slot covers [date_time, date_time + 30 minutes). At 19:10 UTC the active slot starts at 19:00 UTC, not 19:30.
- Compare parsed timestamps, not raw timestamp strings. Convert to Europe/London only for display/calendar calculations; it observes daylight-saving changes.
- The forecast API is intended to include the active half-hour. If it is absent, report missing data rather than substituting a future slot.
- 20 p/kWh = £0.20/kWh. Negative prices are valid. Standing charges are not included in these unit-rate examples.
- Published rows commonly have equal central, low and high values. A current high-band sensor is therefore not necessarily different from the current price.

## Failure handling and safe automations

Validate status, JSON shape, numeric values, timestamps, and target-slot coverage. Handle timeouts, 202, 4xx, 5xx, empty arrays, and stale responses. Do not use price zero as a fallback. Never relabel a prediction as confirmed. Check the confirmed rate again before a cost-sensitive action, use spending/safety limits, and choose an explicit safe state for unavailable data.

When reporting an API issue include the endpoint, region, UTC request time, expected slot and a small redacted response. Do not attach private logs or credentials.
