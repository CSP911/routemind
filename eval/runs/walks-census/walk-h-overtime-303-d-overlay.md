1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D4, hours H1, place P4, what multiplier applies and what rounding for minutes?" --member /v1/regions/payroll "overtime multiplier likely a payroll pay rule" --member /v1/regions/attendance "day/hours/place dimensions sound like attendance/overtime tracking"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3372f9 --outcome answered --used /v1/regions/attendance /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4/body

2. **Answer**
Multiplier: 2.73x. Minutes are rounded to the nearest 5 minutes.

3. **Source**
/v1/regions/attendance
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4/body

4. **Notes**
The top-level table row for /v1/regions/payroll looked equally plausible at first glance since overtime is a pay concept, but a warning file in that region (`hard-moved-overtime`) states overtime premiums moved to attendance on 2026-01-01 — so payroll was a dead end. The attendance region's `sec-hard-overtime` table is explicitly marked as THE CURRENT overtime rate table in force from 2026-01-01, replacing two older versions (`hard-overtime-v2` and `overtime-rate-table`); since today is 2026-09-21, the current table applies and I did not need to consult the superseded versions or the legend-revision warning file. The row address for D4/H1/P4 existed exactly as needed, so no legend lookups (day/hours/place code definitions) were required either — the exact combination was already listed as its own row.
