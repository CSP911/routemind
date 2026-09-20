1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body

2. **Answer**: Multiplier is 1.35x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body

4. **Notes**: The path was straightforward once at /v1/regions/attendance — the description there explicitly calls out "overtime, night and holiday hours pay, by day type, hours and place (current table since 2026-01-01)," pointing to `sec-hard-overtime` over its superseded siblings `hard-overtime-v2` and the legend-revision note. The only place to be careful was not grabbing an older version: the table listing shows `hard-overtime-legend-revision`, `hard-overtime-v2`, and the current `sec-hard-overtime` side by side, and today's date (2026-09-20) falls within the current table's stated force period (from 2026-01-01), so the current row was the right one to read. The row address itself was printed verbatim by the table listing (day-d1-hours-h2-place-p2), so no construction was needed.
