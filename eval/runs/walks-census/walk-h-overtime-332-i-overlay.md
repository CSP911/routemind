1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two in the morning, eleven hours, on standby at home: what multiplier applies, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding are payroll rules" --member /v1/regions/attendance "standby at home may be defined as an attendance category"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_227630 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body

2. **Answer**: Multiplier 3.06x, minutes rounded to the nearest 20 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which version to use for a 2026-09-20 date)
- /v1/nodes/hard-overtime-legend-day/body (two in the morning → day D4)
- /v1/nodes/hard-overtime-legend-hours/body (eleven hours → hours H4)
- /v1/nodes/hard-overtime-legend-place/body (on standby at home → place P3)
- /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body (the multiplier and rounding rule)

4. **Notes**: The question's terms are lifted almost verbatim from the three legends ("two in the morning", "eleven hours", "on standby at home"), so mapping to codes D4/H4/P3 was unambiguous once the legends were read — no nearest-entry guessing needed here. The one place this could have gone wrong is overtime having three superseded versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`); the legend-revision warning page makes clear the current table only applies from 2026-01-01 onward, and the question's implicit date (today, 2026-09-20/21) falls in that range, so `sec-hard-overtime` was correct. Had this been a 2025-dated question I'd have needed `hard-overtime-v2` instead — worth double-checking the date on any overtime question before picking a table. Also note: overtime premiums are documented under attendance's `sec-hard-overtime`, not under payroll (a payroll-region file, `hard-moved-overtime/body`, warns of this move as of 2026-01-01) — starting the search in payroll would have been a dead end.
