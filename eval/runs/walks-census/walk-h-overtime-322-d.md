1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body

2. **Answer**: Multiplier 2.94x; minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body

4. **Notes**: The attendance region listed both a current overtime table (`sec-hard-overtime`, in force from 2026-01-01) and superseded versions (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an older `overtime-rate-table`), plus a `hard-overtime-legend-revision` page explaining which version covers which dates. Since today (2026-09-20) falls within the current table's validity window, I went straight to `sec-hard-overtime` without needing the revision legend — but it would have been easy to grab a superseded row by mistake if the "64 rows" table hadn't clearly labeled D4/H3/P3 combinations by exact address. No ambiguity in the final lookup itself: the row address matched the question's day/hours/place codes exactly.
