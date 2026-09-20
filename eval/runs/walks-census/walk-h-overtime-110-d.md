1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body

2. **Answer**: Multiplier 1.80x; minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body

4. **Notes**: The attendance area lists three versions of the overtime rate table (current since 2026-01-01, a superseded 2024-07-01–2025-12-31 version `hard-overtime-v2`, and an older `overtime-rate-table`), flagged by a "WARNING" legend-revision file. It would have been easy to grab a stale multiplier from one of the superseded nodes — I picked `sec-hard-overtime`, explicitly marked as the table in force from 2026-01-01, which matches today's date (2026-09-20). The row address itself directly encoded the D2/H2/P1 qualifiers, so no legend lookup (day/hours/place definitions) was needed once the row was located — the question only asked for the multiplier and rounding rule, both given directly in the row body.
