1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, six hours, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding likely documented under payroll"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay add --id ov_2026-09-21_531424 --address /v1/regions/attendance --why "payroll node says overtime premiums moved to attendance sec-hard-overtime as of 2026-01-01; Liberation day 2026 falls after that date"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_531424 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body

2. **Answer**: Multiplier 2.46x; minutes rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body

4. **Notes**: The first hop naturally lands on payroll (multiplier/rounding sound like a payroll question), but the payroll table opens straight onto a warning node (`hard-moved-overtime`) saying overtime premiums were moved to attendance's `sec-hard-overtime` for anything dated 2026-01-01 or later — the old payroll page (`payslip-overtime`) was never withdrawn and would have given a wrong, superseded answer if read instead. Liberation Day 2026 is after that cutover, so the pivot to attendance was required. Inside attendance there's a second trap: `hard-overtime-v2` (superseded, in force 2024-07-01 to 2025-12-31) sits right next to the current `sec-hard-overtime` table with very similar names — easy to grab the wrong one if not reading the "THE CURRENT ... TABLE" marker carefully. Mapping the three qualifiers required all three legend files (day/hours/place), each of which states plainly it's the only place the mapping is written — "Liberation Day" maps directly to D3, "six hours" to H3, "on standby at home" to P3, giving row d3-h3-p3 with no ambiguity or nearest-match guessing needed.
