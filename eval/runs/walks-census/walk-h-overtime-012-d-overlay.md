1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H2, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime multipliers and rounding rules are likely part of attendance region"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c08e44 --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body

2. **Answer**: Multiplier 1.38x; minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/sec-hard-overtime (table), /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body (document with the figures)

4. **Notes**: The overlay's only member was the region-level /v1/regions/attendance table, picked on a guess since day/hours/place-coded overtime rules sounded like an attendance concern. From there `table /v1/nodes/sec-hard-overtime` turned out to hold exactly 64 rows, one per day/hours/place combination, with an exact row named `hard-overtime-row-day-d1-hours-h2-place-p3` — no interpretation needed, so I read it directly instead of adding it as an overlay member first. When closing, the CLI flagged both addresses used as "reached" rather than "used," since I navigated to them without formally adding them as overlay members — worth remembering that overlay membership and actual navigation path aren't automatically the same thing. The table's own note confirms this is the current version (in force from 2026-01-01, i.e. current as of today 2026-09-20/21); there are superseded versions (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an even older `overtime-rate-table`) called out in `hard-overtime-legend-revision`, but since the question didn't specify a date, using the currently-in-force table was the correct and only reasonable choice — no need to open the legend-revision doc.
