1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Saturday, three hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/hours rules likely live here" --member /v1/regions/payroll "overtime multiplier and pay rounding could be defined in payroll rules"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a31acf --outcome answered --used /v1/regions/attendance /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body

2. **Answer**: Multiplier 1.89x. Minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
/v1/nodes/hard-overtime-legend-hours/body (three hours → hours H2)
/v1/nodes/hard-overtime-legend-place/body (from home → place P4)
/v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body (the answer: 1.89x, nearest 10 minutes)

4. **Notes**: The overtime table (`sec-hard-overtime`) is coded by three separate legends (day, hours, place) rather than plain language, so each of "Saturday", "three hours", and "from home" had to be translated through its own legend before the row address could be built — none of the three could be guessed directly. The table's warning that overtime rate "has THREE versions with different" rules made me check the effective-date note on the row before trusting it: this table is in force from 2026-01-01, and today is 2026-09-20, so the current version applies and no older version (`hard-overtime-v2` or `overtime-rate-table`) needed to be consulted. I initially also pulled in /v1/regions/payroll as a candidate area, since overtime pay sounded like it could live there, but `hard-moved-overtime/body` in that same working set confirms overtime premiums moved out of payroll into attendance as of 2026-01-01, so payroll was a dead end I didn't need to read further.
