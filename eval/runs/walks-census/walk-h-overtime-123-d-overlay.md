1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D2, hours H3, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table since 2026-01-01, by day/hours/place" --member /v1/nodes/hard-overtime-legend-revision "warns overtime rate has three versions, need to confirm which covers today 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_105303 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body

2. **Answer**: Multiplier 2.01x; minutes rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body

4. **Notes**: The overtime rate table has three superseded/current versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), each covering a different date range, and the current table's own row explicitly says nothing about having replaced anything — so I checked the legend-revision page first to confirm today's date (2026-09-20/21) falls under the current table (`sec-hard-overtime`, in force from 2026-01-01) before trusting the D2/H3/P4 row under it. Skipping that check would have been easy to get away with here since the current table is also the newest, but the legend explicitly warns that reaching for the newest is wrong for dates before 2026-01-01 — worth verifying rather than assuming. No other ambiguity: the three qualifiers (day D2, hours H3, place P4) matched a single row directly under the attendance region's current overtime table.
