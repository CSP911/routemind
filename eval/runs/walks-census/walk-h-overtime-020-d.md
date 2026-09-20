1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body

2. **Answer**: Multiplier 1.44x; minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body

4. **Notes**: The `/v1/regions/attendance` table listed both a current overtime table (`sec-hard-overtime`, in force from 2026-01-01) and two superseded versions (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an older `overtime-rate-table`), plus a `hard-overtime-legend-revision` file explaining which version covers which dates. Since the question gave no date and today (2026-09-20) falls under the current table, I went straight to `sec-hard-overtime` without opening the legend-revision file — worth flagging in case the question intended a historical rate instead of the current one. The row for day D1/hours H3/place P1 existed as an exact, individually-addressed row (one of 64 in the table), so no interpolation or legend lookup (day/hours/place code legends) was needed to resolve the codes themselves.
