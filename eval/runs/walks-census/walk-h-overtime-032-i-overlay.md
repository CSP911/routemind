1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "An ordinary tuesday, eleven hours, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day/hours/place, likely covers standby at home multiplier and rounding" --member /v1/nodes/hard-overtime-legend-revision/body "warns which overtime version covers which dates, need to confirm 2026-09-20 falls under current table"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2cffa4 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body

2. **Answer**: Multiplier is 1.62x; minutes are rounded to the nearest 20 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (an ordinary Tuesday → day D1)
- /v1/nodes/hard-overtime-legend-hours/body (eleven hours → hours H4)
- /v1/nodes/hard-overtime-legend-place/body (on standby at home → place P3)
- /v1/nodes/hard-overtime-legend-revision/body (confirms 2026-09-20 falls under the current table, sec-hard-overtime, in force from 2026-01-01)
- /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body (row with the multiplier and rounding: 1.62x, nearest 20 minutes)

4. **Notes**: The three qualifiers (day, hours, place) are each translated through a separate legend page rather than being obvious from the question's wording — "eleven hours" maps to "H4" only via the hours legend, and "on standby at home" maps to "P3" (distinct from "from home" = P4, a nearby trap). The overtime subject also has three superseded/current versions keyed by date, and the legend-revision page explicitly warns not to assume the newest applies for pre-2026 dates and not to assume the oldest is current just because it lacks a "superseded" notice — today's date (2026-09-20) does fall under the current table, so no correction was needed here, but this is exactly the kind of question where guessing the current table without checking the revision legend would have been an unverified assumption.
