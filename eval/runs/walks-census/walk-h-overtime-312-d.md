1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body

2. **Answer**: Multiplier is 2.82x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p3/body

4. **Notes**: The payroll area's landing table warns up front that overtime premium rates moved to attendance on 2026-01-01, so the payroll page (`hard-moved-overtime`) is a dead end for this figure — worth checking first only to confirm the redirect, not to read further. The attendance area then lists two overtime tables: `hard-overtime-v2` (superseded, 2024-07-01 to 2025-12-31) and `sec-hard-overtime` (current, from 2026-01-01). Since today's date is 2026-09-20, the current table is the right one — it would have been easy to grab the superseded version by mistake since both are listed side by side with similar names. `sec-hard-overtime` expands into 64 rows (4 days × 4 hour bands × 4 places), but the row address is a direct, literal match for D4/H2/P3, so no legend lookup (day/hours/place definitions) was needed once the exact row was visible in the table listing.
