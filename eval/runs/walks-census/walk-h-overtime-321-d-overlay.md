1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D4, hours H3, place P2, what multiplier applies, and to what rounding are minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-legend-revision/body "warns overtime rate has three versions with different date ranges - need to confirm which version and what D4/H3/P2 codes mean"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_abee23 --outcome answered --used /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body /v1/nodes/hard-overtime-legend-revision/body

2. **Answer**: Multiplier 2.91x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body
/v1/nodes/hard-overtime-legend-revision/body

4. **Notes**: Overtime rates are no longer in payroll — a warning file there (`hard-moved-overtime`) redirects to attendance as of 2026-01-01, which is where the real answer lives. Attendance itself lists three overtime tables (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) covering different date ranges, and the legend-revision file is explicit that reaching for the newest one is only correct if the question's date is on or after 2026-01-01 — for a 2025-dated question the middle table would be the right one instead. Today's date (2026-09-21) and the row's own "in force from 2026-01-01" note both confirm the current table applies here, so I didn't need to fall back to the older two-qualifier or one-qualifier versions. The overlay close command flagged the row address as "reached" rather than "member" — it was never added as an explicit `--member`, only surfaced as a child row when the table under `sec-hard-overtime` printed; the legend-revision address I did add directly matched as a member. Doesn't affect the answer, just worth noting for how the overlay bookkeeping works.
