# Agile Forecast Community

Documentation, integration examples, issue reporting, and helpful hints for [Agile Forecast](https://agileforecast.co.uk).

**This repository does not contain the application or forecasting model. They remain private.** It provides ways to use the public API and contribute integrations, not to reproduce the forecasting engine.

## Start here

- [API guide](docs/api.md): endpoints, regions, units, timestamps, and missing data
- [Home Assistant](integrations/home-assistant/README.md): forecast and confirmed-rate sensors
- [Python](integrations/python/README.md): a dependency-free example
- [Report a problem](https://github.com/simonstokes174/agile-forecast-community/issues/new/choose)
- [Questions and helpful hints](https://github.com/simonstokes174/agile-forecast-community/discussions)
- [Contribute an integration](CONTRIBUTING.md)

## Forecasts versus confirmed prices

Predictions and uncertainty bands are estimates, not guaranteed tariffs. Prefer confirmed Octopus rates for cost-sensitive decisions. Never treat missing data as a zero price or an instruction to start equipment. This project is not affiliated with Octopus Energy or Home Assistant.

## Support and scope

The initial examples are project-provided reference examples, not a managed integration or a guarantee of compatibility with every installation. Home Assistant configuration has been template-tested but not tested in every Home Assistant version. Contributions should state their tested versions and limitations. There is no guaranteed support response time.

Use **Issues** for reproducible bugs and concrete integration requests. Use **Discussions** for questions, setups, automation ideas, and sharing hints. Please do not post credentials, account identifiers, or private household information.

## Licence

The original documentation and integration examples in this repository are MIT-licensed; see [LICENSE](LICENSE). This does not license the private Agile Forecast application, forecasting model, trademarks, API service, or third-party data. Public API access does not grant unrestricted rights to redistribute upstream datasets.
