1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H4, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers and minute rounding likely live in payroll rules" --member /v1/regions/attendance "day/hours/place codes suggest attendance/shift rules may define this"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_41eea7 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p2/body

2. **Answer**:
Multiplier: 1.59x. Rounding: to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body (confirmed which version is in force for today's date)
/v1/nodes/sec-hard-overtime (current overtime rate table, in force from 2026-01-01)
/v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p2/body (the row with the actual figures)

4. **Notes**:
The payroll region initially looked like the right place (payroll seemed like where premiums/rounding would live), but it holds only a warning that overtime premiums moved to attendance on 2026-01-01, so the payroll member of the working set turned out to be a dead end — attendance was the real home. Before trusting the current table, I checked the legend-revision warning: overtime rate has three versions (until 2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the oldest version says nothing about being superseded, so reaching for it without checking dates would silently give a stale answer. Today's date (2026-09-20/21) falls in the "2026-01-01 onwards" band, so `sec-hard-overtime` was the correct table, and the row for day D1/hours H4/place P2 gave the figures directly — no ambiguity once the right table was found.
