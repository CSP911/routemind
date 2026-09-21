1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, three hours, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime pay multipliers and payslip line explanations likely live here" --member /v1/regions/attendance "attendance rules may define holiday work and rounding of hours/minutes"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3e32fe --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body

2. **Answer**: Multiplier 2.28x; minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body

4. **Notes**: The overtime rate subject has three versions in force over different date ranges, with an explicit warning that reaching for the newest is wrong for dates before 2026-01-01. The question doesn't give a year for "Liberation day," but since Liberation Day for the current year (2026-08-15) already fell after the 2026-01-01 cutover, and the question offers no reason to think of an older date, the current table (`sec-hard-overtime`) applies — this was the one place I nearly went wrong, since it would have been easy to skip the revision-legend check entirely and just grab whatever table looked current. The three qualifiers (day, hours, place) each required a separate legend lookup to translate the plain-English question into row codes (D3/H2/P1) — none of this mapping is duplicated in the row table itself, so skipping any one legend would have made the row address unguessable.
