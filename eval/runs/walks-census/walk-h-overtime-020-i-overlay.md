1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "An ordinary tuesday, six hours, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table (2026-01-01 onward), likely has multiplier by day type/hours/place" --member /v1/nodes/hard-overtime-legend-revision "warning page listing which overtime version covers which dates, useful for confirming current version"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c487a7 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body

2. **Answer**: Multiplier 1.44x; rounding to the nearest 15 minutes. (In force from 2026-01-01, current as of today 2026-09-21.)

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body

4. **Notes**: The payroll area's table warns up front that overtime premiums moved to attendance on 2026-01-01, so I skipped the old payroll page (`hard-moved-overtime`) entirely and went straight to attendance — that saved a dead-end read. The row address isn't guessable from the question; it has to be built from three separate legend lookups (day type, hour band, place), each of which explicitly says "this table is the only place the mapping is written down." Easy to get wrong: "six hours" maps to H3, not H2 or H4 — the legend bands are ninety minutes/3h/6h/11h, and six hours lands exactly on the H3 entry rather than needing nearest-neighbor guessing. The row confirms it's the current version in force from 2026-01-01 with no later revision, so no version ambiguity here.
