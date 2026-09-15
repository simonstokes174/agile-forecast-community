# Python example

Requires Python 3.10 or later; standard library only.

```sh
python3 forecast.py --region C
```

Select your region with --region (default C = London). Run manually or at a respectful interval, not in a tight loop. The script prints the cheapest future single half-hour starting in the next six hours, excluding the already-started slot. It is not a cheapest contiguous charging window.

It uses timezone-aware UTC timestamps, preserves negative values, checks response structure and numeric values, has a 30-second timeout, and exits non-zero on missing data or request errors. Do not use its output as an unguarded device-control instruction. Confirm published rates before a cost-sensitive action.

Tests can run without network access:

```sh
python3 -m unittest discover -s integrations/python -p 'test_*.py'
```

Run the test command from the repository root.
