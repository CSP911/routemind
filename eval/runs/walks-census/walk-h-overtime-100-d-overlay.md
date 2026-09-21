1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D2, hours H1, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers and rounding rules are typically payroll pay-rate topics"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay add --id ov_2026-09-20_cf101a --address /v1/regions/attendance --why "hard-moved-overtime node says overtime premiums live in attendance's sec-hard-overtime table since 2026-01-01"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_cf101a --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body

2. **Answer**: Multiplier 1.68x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/hard-moved-overtime/body
- /v1/nodes/hard-overtime-legend-revision/body
- /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body

4. **Notes**: The natural first guess is payroll (overtime multipliers "sound like" pay rates), and payroll's table does list an old `payslip-overtime` row — but a warning node (`hard-moved-overtime`) flags that overtime premiums moved to attendance's `sec-hard-overtime` table on 2026-01-01, and payroll's version is only correct before that date. A second trap sits right behind the first: the attendance region itself has three superseded versions of the overtime table (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and a revision-legend node warns that grabbing the newest one is only correct on or after 2026-01-01 — for a 2025 date the middle version would be right instead. Today's date (2026-09-20) put the current table (`sec-hard-overtime`) in force, and its three-qualifier indexing (day/hours/place) matched the question's D2/H1/P1 exactly, confirming it was the right version. Without reading both warning nodes it would have been easy to answer confidently from the wrong (superseded) table.
