1. Commands

./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, three hours, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime/holiday pay multipliers and rounding rules likely live in payroll"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay add --id ov_2026-09-21_0b3b63 --address /v1/regions/attendance --why "overtime premiums moved to attendance region effective 2026-01-01, per hard-moved-overtime note in payroll"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_0b3b63 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body

2. Answer

Multiplier: 2.34x. Rounding: to the nearest 10 minutes.

3. Source

/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body

4. Notes

The obvious first stop was payroll (it's where overtime multipliers used to live), but payroll's own `hard-moved-overtime` note redirects anything dated on or after 2026-01-01 to `sec-hard-overtime` in attendance — Liberation Day 2026 falls after that cutover, so payroll would have given the wrong, superseded figure if I'd stopped there. The row table itself only indexes by codes (D3/H2/P3), not by plain language, so all three legends (day, hours, place) had to be read before the row address could even be identified — "Liberation Day" maps to D3 by falling under "the nearest entry above it" in the day legend's list (Tuesday/Saturday/Liberation Day/two in the morning), which is a slightly odd ordering to trust at first glance but is explicit in the legend's own instructions.
