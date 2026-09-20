1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body

2. **Answer**: Multiplier 1.47x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body

4. **Notes**: The obvious first stop is payroll (overtime sounds like a payslip topic), but the payroll table itself carries a warning that overtime premiums moved to attendance on 2026-01-01, and today (2026-09-20) is after that date, so the payroll-side `payslip-overtime` page would have been the wrong, stale answer. Attendance also still holds two superseded overtime versions (`hard-overtime-v2`, `overtime-rate-table`) alongside the current `sec-hard-overtime` table — easy to grab the wrong one if you don't check the "in force from 2026-01-01" note on the row itself. The row lookup requires translating the plain-English scenario through three separate legend files (day/hours/place) into codes D1/H3/P2; none of the legends repeat each other's mappings, so all three had to be read before the row address could be assembled correctly.
