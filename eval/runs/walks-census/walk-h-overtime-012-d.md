1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body

2. **Answer**: Multiplier is 1.38x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body

4. **Notes**: The payroll region's own table warns that overtime/night/holiday premium rates moved to attendance on 2026-01-01, and that the payroll page still listing them is the old rule — so I didn't open payroll's now-superseded overtime file and went straight to attendance instead. Inside attendance, there were two candidate row-tables: `hard-overtime-v2` (superseded, in force 2024-07-01 to 2025-12-31) and `sec-hard-overtime` (current, in force from 2026-01-01). Since today's date is 2026-09-20, the current table is the correct one — easy to pick the wrong one if you grab the first "overtime" hit without checking the effective-date warnings. Once inside `sec-hard-overtime`, the row address for D1/H2/P3 was printed exactly, no construction needed.
