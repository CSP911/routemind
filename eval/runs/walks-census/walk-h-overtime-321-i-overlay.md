1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two in the morning, six hours, out at a client's office: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime rules, hours worked, client site work likely covered here" --member /v1/regions/payroll "overtime multiplier / pay calculation likely defined here"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_176256 --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body

2. **Answer**
Multiplier: 2.91x. Rounding: to the nearest 15 minutes. (Current table, in force from 2026-01-01; approval was needed in advance and it counts toward the monthly cap.)

3. **Source**
/v1/nodes/sec-hard-overtime (table)
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body

4. **Notes**
The trap here is the day legend: "two in the morning" is not a time-of-day modifier layered on top of a weekday code — it is itself a day code (D4), distinct from D1 (ordinary weekday), D2 (Saturday), D3 (holiday). I almost went looking for a separate "late night" multiplier or a night-shift premium table, but the legend is explicit that the three qualifiers (day, hours, place) are all that select a row, so "2am" simply resolves to D4 on its own. The other two legends were unambiguous exact matches: "six hours" = H3, "out at a client's office" = P2. There was a hard-overtime-legend-revision warning that three versions of this table exist; since today (2026-09-21) falls after the 2026-01-01 effective date of the current table (sec-hard-overtime), the superseded hard-overtime-v2 table was correctly not used.
