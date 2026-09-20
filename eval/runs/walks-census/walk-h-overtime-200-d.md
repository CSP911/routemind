1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body

2. **Answer**: Multiplier is 2.16x. Minutes are rounded to the nearest 5 minutes. (Current table, in force since 2026-01-01.)

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body

4. **Notes**: The walk was straightforward — `/v1/nodes/sec-hard-overtime` lists one row per exact (day, hours, place) combination, so D3/H1/P1 mapped directly to `hard-overtime-row-day-d3-hours-h1-place-p1` with no interpretation needed. The one thing worth flagging: the attendance table's listing explicitly warned that overtime rate "has THREE versions with different" rules, with `hard-overtime-v2` (2024-07-01 to 2025-12-31) and `overtime-rate-table` (older) both still present alongside the current `sec-hard-overtime` table effective 2026-01-01. It would be easy to grab a row from the wrong version if scanning by name alone rather than checking the "THE CURRENT ... TABLE" marker. Today's date (2026-09-20) falls within the current table's validity window, so no version confusion here, but this is the trap to watch for on any similarly-phrased question that doesn't specify "current."
