1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body

2. **Answer**: Multiplier is 2.52x. Minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body

4. **Notes**: The attendance area lists both a current overtime table (`sec-hard-overtime`, in force from 2026-01-01) and two superseded versions (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an older `overtime-rate-table`), plus a legend-revision note flagging three total versions. Today's date (2026-09-20) falls under the current table, so `sec-hard-overtime` was the correct pick, but it would have been easy to grab a superseded row instead without checking the effective-date labels. Within `sec-hard-overtime` the row addresses are systematically named by day/hours/place code, so once the legend structure was clear, finding the exact D3/H4/P1 row was unambiguous — no need to open the legend files since the question already gave codes rather than plain-language day/hours/place descriptions.
