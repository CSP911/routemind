1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D4, hours H4, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/time multiplier rules likely live under attendance" --member /v1/regions/payroll "pay multiplier and rounding could be a payroll rule"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_0106c2 --outcome answered --used /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body

2. **Answer**: Multiplier 3.00x; minutes are rounded to the nearest 20 minutes. (This row also requires approval in advance and counts toward the monthly cap.)

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body

4. **Notes**: The top-level table only names broad regions (attendance, payroll, etc.), not overtime specifically, so I put both attendance and payroll into the working set as candidates before narrowing. Overtime rate turned out to live entirely under attendance's `sec-hard-overtime` table. That table's row listing has a `WARNING` sibling node (`hard-overtime-legend-revision`) flagging that overtime rates have had three versions over time with different multipliers/rounding — I didn't need to open it because `sec-hard-overtime` is explicitly labeled "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," today's date (2026-09-21) falls inside that range, and the row itself repeats "In force from 2026-01-01" — so the current-version row was the correct and only one to read. The row addresses are fully enumerated by day/hours/place code (e.g. `hard-overtime-row-day-d4-hours-h4-place-p1`), so the exact requested combination was a direct, unambiguous lookup with no interpretation needed. The overlay close reported the answer address as "reached" rather than a named member, since I read it directly from the table listing instead of adding it to the overlay as a member first — worth knowing that overlays track only what's explicitly added as a member, not everything read along the way.
