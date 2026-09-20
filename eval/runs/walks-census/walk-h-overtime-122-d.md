1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body

2. **Answer**: Multiplier is 1.98x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate versions applies for today's date, 2026-09-20)
- /v1/nodes/sec-hard-overtime (table listing the row addresses by day/hours/place)
- /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body (the figures)

4. **Notes**: The payroll region's overview explicitly warns that overtime premiums moved to attendance on 2026-01-01, and the old payroll page (`hard-moved-overtime`) is superseded — easy to grab a stale multiplier there if you stop at the first hit. Within attendance, there are three versions of the overtime table (pre-2024-07-01, 2024-07-01–2025-12-31 as `hard-overtime-v2`, and 2026-01-01-onward as `sec-hard-overtime`), and the legend-revision file is explicit that the newest is not always right — for a 2025-dated question the middle version would be correct instead. Since today is 2026-09-20, the current table (`sec-hard-overtime`) was the right pick, and it happened to have an exact-match row for D2/H3/P3, so no interpolation or legend lookups for day/hours/place codes were needed.
