1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D2, hours H3, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers and rounding rules are payroll topics"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_059484 --address /v1/regions/payroll --why "overtime moved to attendance on 2026-01-01, per hard-moved-overtime notice"
./bench/rmcli.py overlay add --id ov_2026-09-20_059484 --address /v1/regions/attendance --why "overtime multipliers now live in attendance table sec-hard-overtime"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_059484 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body

2. **Answer**: Multiplier is 1.95x. Minutes are rounded to the nearest 15 minutes. (This is the current rule, in force from 2026-01-01; today's date is 2026-09-20/21, so it applies.)

3. **Source**:
- /v1/nodes/hard-moved-overtime/body (confirmed overtime rules live in attendance, not payroll, as of 2026-01-01)
- /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p2/body (the multiplier and rounding figures)

4. **Notes**: My first instinct was to pick payroll as the region, since "multiplier" and payslip-line style figures read as a payroll question. Payroll's own table has a row `payslip-overtime` ("Overtime, night and holiday premiums") that looks like a plausible direct hit, but the region's `hard-moved-overtime` notice warns that overtime premiums moved to attendance's `sec-hard-overtime` table as of 2026-01-01 and that the payroll row is only correct for dates before that. Since today is 2026-09-20/21, using the payroll row would have given a stale (and possibly wrong) multiplier/rounding pair. Had to backtrack out of payroll and into attendance to find the actual current table. Within `sec-hard-overtime` there were also two older superseded versions (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an implied `overtime-rate-table` before that) — easy to grab the wrong version if not reading the "in force from 2026-01-01" qualifier on `sec-hard-overtime` and the row body itself.
