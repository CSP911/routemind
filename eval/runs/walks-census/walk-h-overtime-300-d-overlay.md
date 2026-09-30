1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "For day D4, hours H1, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-legend-revision/body "explains which version of the overtime table covers which dates"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_5f728d --outcome answered --used /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body /v1/nodes/hard-overtime-legend-revision/body

2. **Answer**: Multiplier 2.64x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body
/v1/nodes/hard-overtime-legend-revision/body

4. **Notes**: Both payroll and attendance mention overtime — payroll's table page has a WARNING that overtime premiums moved to attendance on 2026-01-01, which confirms attendance is the right region and rules out chasing the old payroll rule. The bigger trap is version: overtime rate has three superseded/current versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), each indexed by a different number of qualifiers (one, two, three respectively). A D4/H1/P1-style three-qualifier address only exists under the current (2026-01-01 onwards) table, so grabbing the newest table was correct here, but I checked the revision legend explicitly rather than assuming, since the legend itself warns that reaching for the newest is wrong for dates before 2026-01-01 and that the oldest page never announces its own replacement.
