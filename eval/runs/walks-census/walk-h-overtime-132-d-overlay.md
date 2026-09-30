1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D2, hours H4, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier/rounding likely a pay rule" --member /v1/regions/attendance "overtime hours tracked as attendance/time rule"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_2c7ecd --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body

2. **Answer**: Multiplier is 2.10x. Minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-legend-revision/body, /v1/nodes/sec-hard-overtime, /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body (in that order of use)

4. **Notes**: The opening table split "how much a business trip pays" between expense/payroll, but overtime rate itself lives under attendance, not payroll — a file at /v1/nodes/hard-moved-overtime/body in the payroll region explicitly warns that overtime premiums moved out of payroll to attendance on 2026-01-01, which confirmed the attendance region was the right branch and payroll was a dead end for this question. The bigger trap was versioning: overtime rate has three superseded-but-never-marked-withdrawn versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the oldest one says nothing about being replaced, so grabbing the first hit without checking the legend-revision page could easily have produced a stale multiplier. The question gives D/H/P codes (not a calendar date), and today (2026-09-20/21) falls after the 2026-01-01 cutover, so the current three-qualifier table (`sec-hard-overtime`) was the correct one — confirmed by reading the revision legend before picking a row. The row address matched the D2/H4/P3 qualifiers exactly, so no legend lookup for day/hours/place codes was needed once the row was found.
