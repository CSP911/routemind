1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body

2. **Answer**: Multiplier 2.46x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p3/body

4. **Notes**: The payroll region's overview page explicitly warns that overtime premiums moved to attendance on 2026-01-01, which kept me from reading the stale payroll page as the answer. Inside attendance, there are three superseded versions of the overtime table (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime`); the legend-revision warning node made clear `sec-hard-overtime` is the one in force for today's date (2026-09-20), so I didn't need to open the older versions. The row table itself gives no clue which of the 64 addresses to pick without the three legend files — "Liberation Day", "six hours", and "on standby at home" only resolve to day D3 / hours H3 / place P3 after reading the day, hours, and place legends respectively, and each legend states it is "the only place the mapping is written down," so skipping any one of them would have made the row address unguessable rather than just harder.
