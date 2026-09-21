1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H4, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding are payroll rules"
./bench/rmcli.py overlay remove --id ov_2026-09-20_0f43bd --address /v1/regions/payroll --why "overtime premiums moved to attendance as of 2026-01-01, this question is current"
./bench/rmcli.py overlay add --id ov_2026-09-20_0f43bd --address /v1/regions/attendance --why "hard-moved-overtime notice points to sec-hard-overtime in attendance for current rules"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0f43bd --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body

2. **Answer**: Multiplier is 1.62x; minutes are rounded to the nearest 20 minutes. (In force from 2026-01-01, the current table; approval is needed in advance and it counts toward the monthly cap.)

3. **Source**:
- /v1/nodes/hard-moved-overtime/body
- /v1/nodes/hard-overtime-legend-revision/body
- /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body

4. **Notes**: My first instinct was to open the payroll region, since overtime multipliers sound like a payroll concept — but the payroll table's first row was a warning (`hard-moved-overtime`) saying overtime premiums moved to attendance's `sec-hard-overtime` as of 2026-01-01, with payroll's `payslip-overtime` only correct for dates before that. Since today is 2026-09-20/21, I had to pivot to attendance. Inside attendance there was a second trap: `hard-overtime-legend-revision` warns the overtime-rate subject has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and none were withdrawn — the oldest doesn't even say it was replaced. Only by reading that warning could I be sure `sec-hard-overtime` (three qualifiers: day/hours/place) is the one that applies now, rather than the two-qualifier `hard-overtime-v2`. Once inside `sec-hard-overtime`, the row for D1/H4/P3 was named exactly as printed, so no ambiguity there. The overlay close output flagged the three sources as "reached ... somewhere the overlay never named" since I navigated to them via table/read rather than adding them as explicit overlay members — worth noting in case that distinction matters for scoring.
