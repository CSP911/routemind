1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D1, hours H3, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table (2026-01-01 onward), by day/hours/place — matches D1/H3/P4 coding" --member /v1/nodes/hard-overtime-legend-revision/body "warns overtime rate has three versions with different date ranges — need to confirm which version is current for 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_db74cb --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body

2. **Answer**: Multiplier 1.53x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body
- /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body

4. **Notes**: The overtime rate subject has three superseded versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), each with a different date range and indexing scheme — the legend-revision page warns explicitly that grabbing the newest one is wrong for anything dated before 2026-01-01. Today (2026-09-20) falls in the current table's range (2026-01-01 onward, `sec-hard-overtime`), so that was the right one to use, but this is exactly the kind of question where picking the wrong version silently gives a plausible-looking wrong multiplier. Creating the overlay's initial member list conveniently surfaced the individual per-row addresses (one per D/H/P combination) under the `sec-hard-overtime` table, so the exact row `hard-overtime-row-day-d1-hours-h3-place-p4` was directly visible without needing to open the table itself — the close command flagged this row as "reached" rather than a named overlay member since I only added the parent table and the legend page as `--member`, not the leaf row.
