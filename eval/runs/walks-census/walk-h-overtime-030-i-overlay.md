1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Ordinary Tuesday, 11 hours at desk: overtime multiplier and minute rounding rule?" --member /v1/regions/payroll "overtime multiplier and pay rules likely live in payroll" --member /v1/regions/attendance "attendance may define ordinary working hours / overtime thresholds and time rounding"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c314d7 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body

2. **Answer**
Multiplier: 1.56x. Rounding: to the nearest 20 minutes. (Approval needed in advance: yes; counts toward the monthly cap: yes.)

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body

4. **Notes**
Overtime premiums were flagged in payroll as having moved to attendance on 2026-01-01 (/v1/nodes/hard-moved-overtime/body appeared as a warning row under payroll), which confirmed attendance was the right region rather than payroll — payroll would have been a dead end. The overtime rate table (/v1/nodes/sec-hard-overtime) is coded by three independent legends (day, hours-band, place) that must each be resolved before picking a row; it would be easy to guess a row address directly, but the legends are the only place the mapping from plain language to codes (D1/H4/P1) is written, and the instructions are explicit that no smaller table exists than what the legends give. There are three historical versions of the overtime table (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime` in force from 2026-01-01); since today is 2026-09-21, the current table is the right one, but this is worth double-checking on any question with an ambiguous or past-dated scenario. "Eleven hours" maps exactly to hours band H4, so no nearest-entry judgment call was needed there.
