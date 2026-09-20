1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body

2. **Answer**: Multiplier is 1.53x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body

4. **Notes**: The payroll region's overview table flags that overtime premium rates moved to attendance on 2026-01-01, which is exactly the current-dated scenario here — following the payroll page's old rate would have been wrong. The bigger trap was the place legend: "from home" (P4) and "on standby at home" (P3) are two different rows with presumably different multipliers, and it would be easy to skim past "at home" and pick the standby row by mistake. All three legend lookups (day, hours, place) matched their inputs exactly ("an ordinary Tuesday", "six hours", "from home"), so no nearest-entry judgment calls were needed.
