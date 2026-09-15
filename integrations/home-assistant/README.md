# Home Assistant

This package uses the built-in REST and Template integrations. It is a reference configuration, not a custom component or HACS integration. No API key is needed.

## Install

1. Save [agile_forecast.yaml](agile_forecast.yaml) in your Home Assistant config directory under packages/.
2. Replace C in **both** resource URLs with your region code from [the API guide](../../docs/api.md).
3. Enable packages in configuration.yaml. Merge this into an existing homeassistant block; do not create duplicate YAML keys:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

4. Run Home Assistant's configuration check, then restart Home Assistant.
5. Confirm the two API Data entities exist with the expected prices/confirmed_rates attributes. The templates assume sensor.agile_forecast_api_data and sensor.agile_confirmed_api_data. If Home Assistant assigns different entity IDs, update the template references.

Remove or disable the older standalone REST price sensors before installing this replacement: the four public sensor unique IDs are intentionally unchanged. Existing custom entity names may be retained by the entity registry.

## Sensors

- Agile Forecast Current Price: active half-hour central price.
- Agile Forecast Current High: active half-hour upper band (often identical to current price when already published).
- Agile Forecast Cheapest Next 6h: minimum **single half-hour** prediction whose start is between now and six hours ahead. Excludes the already-started slot. It is not a six-hour average or a cheapest contiguous charging window.
- Agile Confirmed Current Price: published price for the active half-hour.

Two supporting API Data sensors hold response attributes. Their state is the last successful template-render time, not a price. Forecast data refreshes every 30 minutes; confirmed rates every 10 minutes. The derived sensors use now() so they re-evaluate each minute, including at half-hour boundaries, without additional API calls. Values may change up to roughly a minute after a boundary.

Missing slots produce an unknown state (not zero). Failed/unavailable raw sensors or data older than two hours make derived sensors unavailable. No automatic substitution of a future slot or forecast for a confirmed price is performed. This is a basic freshness guard, not a service-availability guarantee: confirm the target slot and rate again before sensitive actions.

Avoid recording the large raw attribute arrays if you do not need them; merge these exclusions with your existing recorder settings:

```yaml
recorder:
  exclude:
    entities:
      - sensor.agile_forecast_api_data
      - sensor.agile_confirmed_api_data
```

## Troubleshooting

If cheapest-next-6h works but current sensors do not, inspect whether a row exists for the active half-hour. At 19:10 UTC it must start at 19:00 UTC. Never replace the exact match with the first row. That can silently use a future price.

Check entity IDs, raw attributes, Developer Tools templates, and logs. Preserve negative prices. Do not assign monetary device_class: p/kWh is a price-per-energy unit rather than a currency-only unit. For automations, check has_value(), and use confirmed prices when available. Do not use float(0) as a missing-price fallback.

## Verification status

YAML structure and price templates are checked against synthetic fixtures for active slots, future-only data, negative prices, missing values, and stale data. The example has not been exercised inside a running Home Assistant installation; report your tested Home Assistant version in contributions.

To run the fixture tests from the repository root:

```sh
python3 -m pip install -r requirements-test.txt
python3 -m unittest discover -s integrations/home-assistant -p "test_*.py"
```
