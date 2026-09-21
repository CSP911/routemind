1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A saturday, three hours, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/weekend work rules likely live here" --member /v1/regions/payroll "overtime pay multiplier and rounding could be a payroll rule"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b137f8 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body

2. **Answer**: Multiplier 1.80x; minutes rounded to the nearest 10 minutes. (Row for day D2 / hours H2 / place P1, in force from 2026-01-01, which covers today's date of 2026-09-20.)

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body

4. **Notes**: The overlay's initial members were the two region tables (attendance, payroll), not the actual leaf documents — the walk had to expand into `sec-hard-overtime`'s own table to find the legends and rows, so `overlay close --used` reported those leaf addresses as "reached" rather than formally-tracked members; the answer is unaffected but the overlay tool distinguishes the two. The real trap was the three-versions warning on `hard-overtime-legend-revision`: overtime rate has an old table, a 2024-07-01–2025-12-31 version, and the current one from 2026-01-01, and the doc explicitly says defaulting to the newest is wrong for a 2025-dated question. Today (2026-09-20) is safely inside the current version's range, but I checked the revision note before trusting `sec-hard-overtime` rather than assuming. Separately, `hard-moved-overtime/body` under payroll confirms overtime premiums moved out of payroll into attendance as of 2026-01-01, which is why payroll had nothing for this and attendance was the right region despite the question sounding like a pay question.
