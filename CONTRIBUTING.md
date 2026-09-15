# Contributing

Thank you for helping people use Agile Forecast.

## Welcome contributions

Documentation fixes, Home Assistant configurations, Node-RED flows, small API clients, and tested integration examples. The private application and model are outside this repository; model observations can be discussed, but private implementation access is not provided.

1. Check existing Issues and Discussions.
2. For a substantial integration, describe it in an issue before starting.
3. Fork this repository and add a focused change on a branch.
4. Include a README with setup, supported/tested versions, polling frequency, units, timezone handling, expected outputs, and limitations.
5. Test missing/stale data, negative values, half-hour boundaries, and failures. Confirmed and predicted prices must remain distinguishable.
6. Open a pull request describing the checks you performed.

Use placeholders for configuration. Never include secrets, personal data, database exports, private application code, model artefacts, or code/data you lack permission to redistribute. Do not add an integration that requires disabling device safety protections.

Keep dependencies small. Do not make aggressive requests to the public API in CI. Label whether an example has been tested in the target platform or only with fixtures. Be respectful, explain disagreements with evidence, and do not share others' personal information.

By submitting a contribution, you confirm you have permission to contribute it under this repository's MIT licence. Maintainers may request changes or decline contributions; inclusion does not imply a support guarantee.
