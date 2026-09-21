1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, three hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/holiday work rules, from-home time likely tracked here" --member /v1/regions/payroll "overtime pay multiplier and minute rounding likely defined here"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b83980 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body

2. **Answer**: Multiplier 2.37x; minutes rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-legend-day/body, /v1/nodes/hard-overtime-legend-hours/body, /v1/nodes/hard-overtime-legend-place/body, /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p4/body

4. **Notes**: The overlay's initial members (the attendance and payroll region tables) were never actually read — the useful path was table /v1/nodes/sec-hard-overtime, which sits under attendance but wasn't named as an overlay member itself; the overlay close command flagged all four sources used as "reached... from somewhere the overlay never named," which is accurate but slightly unsettling since I had done the narrowing correctly, just via table drill-down rather than overlay add/remove. The three qualifiers (day/hours/place) each need translation through a separate legend before the row address can be built — "Liberation Day" maps directly to day D3 in the legend, so no ambiguity there; "three hours" maps exactly to hours H2; "from home" maps exactly to place P4 — all three were exact matches, not nearest-entry approximations, so no judgment calls were needed. There is also a superseded row table (hard-overtime-v2, in force 2024-07-01 to 2025-12-31) and an even older `overtime-rate-table`; since today is 2026-09-21/09-20, the current table (in force from 2026-01-01) is correct, but it would be easy to grab the wrong version if not reading the "in force" note on the row itself.
