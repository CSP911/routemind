1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body

2. **Answer**: Multiplier 2.58x; minutes rounded to the nearest 20 minutes. (Approval needed in advance; counts toward the monthly cap.)

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Liberation Day → day D3)
- /v1/nodes/hard-overtime-legend-hours/body (eleven hours → hours H4)
- /v1/nodes/hard-overtime-legend-place/body (on standby at home → place P3)
- /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body (multiplier and rounding)

4. **Notes**: The attendance area listed two overtime rate tables — the current `sec-hard-overtime` (in force since 2026-01-01) and a superseded `hard-overtime-v2` (2024-07-01 to 2025-12-31), plus an even older `overtime-rate-table` referenced in the row's footer. Today's date (2026-09-20) falls under the current table, so I did not need to check the superseded ones, but it would have been easy to grab the wrong version if I hadn't noticed the "SUPERSEDED" / "in force" labels in the table listing. The three legends (day, hours, place) each map a plain-language description to a code, and the row address is built by combining those three codes — none of this is guessable without reading all three legends first, since e.g. "on standby at home" and "from home" are distinct place codes (P3 vs P4) with presumably different multipliers, and it would have been easy to conflate them.
