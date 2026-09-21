1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H2, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding sounds like payroll pay rules" --member /v1/regions/attendance "day/hours/place codes may be attendance overtime rules"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_37e101 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body

2. **Answer**: Multiplier 1.41x; minutes are rounded to the nearest 10 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate versions applies for today's date, 2026-09-20/21 — the current one)
- /v1/nodes/sec-hard-overtime (the current overtime rate table, listing the row for day D1/hours H2/place P4)
- /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body (the row itself, source of the figures)

4. **Notes**: The root table had two plausible starting areas — payroll and attendance — because "multiplier" and "rounding of minutes" sound like a payroll pay-rule question. Payroll turned out to be a dead end: it holds a warning document (`hard-moved-overtime`) stating overtime premiums moved out of payroll to attendance as of 2026-01-01, so payroll no longer carries this rate table. The actual answer lives under attendance (`sec-hard-overtime`). The other near-miss was version selection: overtime rates have three historical versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision doc explicitly warns not to reach for the newest by default — the date on the question decides. Since no date was given in the question but today is 2026-09-20/21, the current table (in force from 2026-01-01) is the correct one, and that's what was used.
