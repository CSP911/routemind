1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D3, hours H4, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding sound like payroll pay-rate rules"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay add --id ov_2026-09-21_ab60b6 --address /v1/regions/attendance --why "hard-moved-overtime notice says overtime premiums moved to attendance sec-hard-overtime effective 2026-01-01"
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ab60b6 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body

2. **Answer**: Multiplier 2.52x; minutes rounded to the nearest 20 minutes. (Current table, in force from 2026-01-01.)

3. **Source**:
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body

4. **Notes**: I started in payroll because "multiplier" and "rounding" read like a pay-rate question, but payroll's own overtime page (`hard-moved-overtime`) immediately warns that overtime premiums moved out of payroll into attendance's `sec-hard-overtime` as of 2026-01-01 — if I'd trusted the first table's placement and gone straight to a payroll overtime row, I'd have answered from a superseded source. Attendance itself then had a second trap: `hard-overtime-legend-revision` shows overtime rate has been written three times (one-qualifier, two-qualifier, and the current three-qualifier version), and warns that reaching for the newest is wrong for dates before 2026-01-01. The question gives three qualifiers (day/hours/place) with no explicit date, which matches the indexing scheme of the current table (`sec-hard-overtime`), so I used that version rather than assuming from today's date alone. No date was stated in the question itself, so the qualifier-count match was the deciding signal, not the current date.
