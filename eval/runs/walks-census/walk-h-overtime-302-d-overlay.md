1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D4, hours H1, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers are typically pay-related" --member /v1/regions/attendance "time/hours tracking and rounding rules likely live here"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_91d870 --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body

2. **Answer**: Multiplier 2.70x; minutes rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/sec-hard-overtime (table listing the current overtime rate rows)
- /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body (the row itself)

4. **Notes**: The initial overlay guessed both payroll and attendance as likely homes, and a payroll-side file (`hard-moved-overtime`) confirms overtime premiums moved out of payroll into attendance on 2026-01-01, so payroll would have been a dead end. The attendance region held a table specifically titled "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01" (`sec-hard-overtime`), plus a legend-revision warning noting three historical versions of the overtime rate exist. Today's date (2026-09-21) falls within the current version's effective range, so no version confusion applied here — but it would be easy to grab a superseded row (`hard-overtime-v2`) by mistake for a question set in an earlier period. The row address itself directly encoded day/hours/place (`hard-overtime-row-day-d4-hours-h1-place-p3`), so no legend lookups for day/hours/place codes were needed.
