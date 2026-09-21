1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H3, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers by day type/hour band/place are usually pay-related" --member /v1/regions/attendance "attendance may define overtime hour bands and rounding rules"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_3bd09a --outcome answered --used /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body

2. **Answer**: Multiplier is 1.47x; minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body

4. **Notes**: The top-level table put both payroll and attendance in play, since overtime pay sounds payroll-related, but a warning row (`hard-moved-overtime`) under payroll flags that overtime premiums moved to attendance on 2026-01-01, so attendance was the right region. Under attendance, `sec-hard-overtime` was clearly labeled "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," and it listed one row per exact (day, hours, place) combination, including a direct hit for day D1, hours H3, place P2 — no interpolation or legend lookup needed since the question already gave codes rather than plain-language values. Also visible were `hard-overtime-legend-revision` and `hard-overtime-v2`, which flag that this table has three historical versions with different rates; today's date (2026-09-20) falls inside the current version's effective range, so no version conflict. Did not need to open the legend files (day/hours/place) since the question specified codes directly rather than descriptions needing translation.
