1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D4, hours H2, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers by day/hour/place sound like payroll pay-rate rules" --member /v1/regions/attendance "day/hour bands could be attendance overtime rules"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8c5712 --outcome answered --used /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body

2. **Answer**: Multiplier is 2.85x. Minutes are rounded to the nearest 10 minutes. (Approval is required in advance and the time counts toward the monthly cap.)

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body

4. **Notes**: The top-level table had no obvious "overtime" row, so I hedged between payroll and attendance as members of the working set — the actual current overtime table (`sec-hard-overtime`) turned out to live under attendance, not payroll. There's a warning node (`hard-moved-overtime`) saying overtime premiums moved out of payroll into attendance on 2026-01-01, which confirms that guess but I didn't need to read it since the row I wanted was already directly addressable once I opened `sec-hard-overtime`. That table's own description ("64 rows indexed by day code and hours code and place code") made it obvious the row would be named `hard-overtime-row-day-d4-hours-h2-place-p4`, and it was printed exactly as such, so no construction of the address was needed. I did not open the superseded versions (`hard-overtime-v2`, `overtime-rate-table`) or the legend files, since the row body itself stated it's in force from 2026-01-01 and today (2026-09-21) falls within that period — no ambiguity there.
