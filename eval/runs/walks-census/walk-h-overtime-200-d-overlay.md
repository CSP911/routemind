1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D3, hours H1, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table, in force from 2026-01-01, by day/hours/place" --member /v1/nodes/hard-overtime-legend-revision "warns overtime rate has three versions with different date ranges - need to confirm which applies today" --member /v1/nodes/hard-overtime-v2 "superseded version 2024-07-01 to 2025-12-31, for comparison/ruling out"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_aea868 --address /v1/nodes/hard-overtime-v2 --why "confirmed current table (2026-01-01 onwards) applies for today's date 2026-09-21; v2 not needed"
./bench/rmcli.py overlay close --id ov_2026-09-21_aea868 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body

2. **Answer**: Multiplier is 2.16x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body

4. **Notes**: The payroll area's overview flags that overtime premiums moved to attendance on 2026-01-01, which correctly redirected the search away from the old payroll page (`/v1/nodes/hard-moved-overtime/body`). Once in attendance, the real trap was the three superseded versions of the overtime rate table (pre-2024-07-01, 2024-07-01–2025-12-31 as `hard-overtime-v2`, and the current `sec-hard-overtime` from 2026-01-01). The legend-revision file explicitly warns that "the oldest says nothing at all about having been replaced" and that reaching for the newest is wrong for dates before 2026-01-01 — since today is 2026-09-21, the current table was correct, but it was worth confirming rather than assuming, so I read the revision file before trusting the row. The overlay's initial listing was very large (67 rows, one per day/hours/place combination) but the exact address `hard-overtime-row-day-d3-hours-h1-place-p1` was printed directly, so no ambiguity there — the row itself contains both the multiplier and rounding rule in one small table, no need to consult the separate day/hours/place legend definitions since D3/H1/P1 were already given as exact codes in the question.
