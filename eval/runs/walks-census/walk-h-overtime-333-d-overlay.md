1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D4, hours H4, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding sound like payroll pay computation rules" --member /v1/regions/attendance "overtime hours and day/place classification may be defined in attendance rules"
./bench/rmcli.py overlay remove --id ov_2026-09-21_7acc4c --address /v1/nodes/insurance --why "not relevant to overtime multiplier"
./bench/rmcli.py overlay remove --id ov_2026-09-21_7acc4c --address /v1/nodes/payroll-desk --why "not relevant"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_7acc4c --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p4/body

2. **Answer**: Multiplier 3.09x. Minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/sec-hard-overtime (table listing the row)
/v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p4/body (the answer)

4. **Notes**: The multiplier and rounding rule are described as "no longer written in payroll" — a warning row (`hard-moved-overtime`) under the payroll region says overtime premiums moved to attendance on 2026-01-01, so starting from the payroll region was a plausible but wrong first guess; the actual current table (`sec-hard-overtime`) lives under attendance. The row address happened to use the exact same day/hours/place codes given in the question (D4/H4/P4), so no legend lookup was needed to translate a plain-language description into codes — that won't be true for every question in this family, and I'd have needed `hard-overtime-legend-day/hours/place` if the question had described the day, hour band, or place in words instead of codes. There are three historical versions of this table (`overtime-rate-table`, `hard-overtime-v2`, and the current one); the row body itself states it is in force from 2026-01-01, and today's date (2026-09-21) falls inside that range, so I did not need to open the separate `hard-overtime-legend-revision` document to confirm currency — I did note its existence in case a future question falls on a boundary date.
