1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Two in the morning, three hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place - in force from 2026-01-01, matches the question's date context (2026-09-20)"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_1539fb --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body

2. **Answer**: Multiplier 2.85x; minutes rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p4/body

4. **Notes**: The question's three clauses map to three separate legend tables, not one — "two in the morning" is a day-type (D4), not a time-of-day modifier on top of whatever weekday it is; the legend literally lists "two in the morning" as its own row mapped to D4, distinct from "an ordinary Tuesday" (D1) or "a Saturday" (D2). It would have been easy to assume D4 meant something like "night shift on a weekday" and go hunting for an actual date, but the legend is explicit and self-contained — no date is needed or given. Payroll's own table warned upfront that overtime premiums moved to attendance on 2026-01-01, which saved a wasted read of the superseded payroll page. Also had to resist reading the H1 row ("about ninety minutes") since three hours is much closer to no listed value than to ninety minutes — but the hours legend lists "three hours" verbatim as H2, so no nearest-neighbor judgment was actually needed.
