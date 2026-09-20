1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p2/body

2. **Answer**: Multiplier is 1.59x. Minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p2/body

4. **Notes**: Straightforward walk. The table headings loudly flag that this domain has three superseded versions of the overtime rate (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime`), which is where I nearly went wrong — it would be easy to grab a stale multiplier from one of the older nodes. `sec-hard-overtime` explicitly states it is "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," and today's date (2026-09-20) falls inside that range, so I used it directly. The table listing at `/v1/nodes/sec-hard-overtime` indexes all 64 day/hours/place combinations, so the row for D1/H4/P2 could be picked exactly by address without needing the legend files.
