1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body

2. **Answer**: Multiplier 2.79x; minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p2/body (version check via /v1/nodes/hard-overtime-legend-revision/body)

4. **Notes**: The attendance area holds three separate versions of the overtime rate table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and current from 2026-01-01), and the legend-revision page explicitly warns that reaching for the newest is wrong for dates before 2026-01-01 and that the oldest version says nothing about being superseded. Today's date (2026-09-20) falls in the current table's range, so `sec-hard-overtime` was correct, but this was the one place the walk could have silently gone wrong if the revision warning weren't checked first. Once in the current table, the row for D4/H2/P2 existed directly (64 rows, one per day/hours/place combination), so no legend lookups for day/hours/place codes were needed — the exact three-qualifier row was listed and read straight away.
