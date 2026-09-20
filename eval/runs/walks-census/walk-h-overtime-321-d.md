1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body

2. **Answer**: Multiplier is 2.91x. Minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body (with /v1/nodes/hard-overtime-legend-revision/body used to confirm this is the correct version for today's date, 2026-09-20).

4. **Notes**: The attendance area holds three separate overtime-rate tables (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend page explicitly warns that the oldest version never says it was superseded — so grabbing the first "overtime rate" table found without checking dates would have silently given a stale answer. Today's date (2026-09-20) falls in the 2026-01-01-onward current table (`sec-hard-overtime`), which is also the only one of the three indexed by all three qualifiers (day, hours, place) that the question specifies, so it was a clean match once the version was confirmed. The D4/H3/P2 row existed directly under that table with no further disambiguation needed.
