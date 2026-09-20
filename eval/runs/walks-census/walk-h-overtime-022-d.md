1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body

2. **Answer**: Multiplier is 1.50x. Minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body

4. **Notes**: The table at /v1/nodes/sec-hard-overtime lists a row per exact (day, hours, place) combination — d1/h3/p3 matched a row address directly, so no interpretation of the legends (day/hours/place definitions) was needed. The one thing worth flagging: this table is explicitly dated "in force from 2026-01-01" and warns of two older superseded versions (`hard-overtime-v2` for 2024-07-01–2025-12-31, and `overtime-rate-table` before that). Today is 2026-09-20, so the current table is the right one — but it would be easy to grab the wrong version if the "in force from" date weren't checked, since the older superseded files are still present in the attendance area alongside the current one and are not otherwise distinguished until you open the file.
