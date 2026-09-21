1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D3, hours H4, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers and pay rules are typically payroll topics" --member /v1/regions/attendance "day/hour/place codes could be attendance shift definitions"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_1b2e1a --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body

2. **Answer**: Multiplier 2.61x; minutes rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body

4. **Notes**: The initial overlay guess included both payroll and attendance, since "multiplier" and "pay" sound like payroll territory. But the payroll region itself carries a hard warning (`/v1/nodes/hard-moved-overtime/body`) that overtime premiums moved out of payroll to attendance on 2026-01-01 — so payroll would have been the wrong place to read from even though it looked plausible. The real table, `sec-hard-overtime`, lives under attendance and is explicitly marked as "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," with two superseded versions (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an older `overtime-rate-table`) flagged by `hard-overtime-legend-revision`. Today's date (2026-09-21) falls inside the current version's range, so no version-switch was needed, but it would have been easy to grab a stale row without checking that. The overlay's `remove` command rejected addresses that were plainly listed in the printed table (e.g. `/v1/nodes/insurance`) with a 404 "not in this overlay" — worth noting as a rough edge, though it didn't block reaching the answer since the row was found directly via the table/read path rather than by trimming the overlay.
