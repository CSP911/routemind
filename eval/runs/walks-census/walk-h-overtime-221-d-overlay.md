1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D3, hours H3, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day/hours/place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-legend-revision/body "warns which version covers which dates, need to confirm current version applies"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a076a7 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body

2. **Answer**: Multiplier 2.43x; minutes rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed the current, 2026-01-01-onward table applies for today's date)
- /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p2/body (the figures)

4. **Notes**: The overtime subject has three superseded versions (oldest, a 2024-07-01–2025-12-31 middle version `hard-overtime-v2`, and the current `sec-hard-overtime` from 2026-01-01). The legend-revision page warns the oldest version never says it was replaced, so it's easy to grab it by mistake — checking that page against today's date (2026-09-21) before reading the row was necessary, not optional. The overlay's member list only had the region-level `sec-hard-overtime` table address, not the individual row; the table listing itself expanded into all D×H×P row addresses, and I read the exact D3/H3/P2 row directly off that list rather than drilling through `sec-hard-overtime` again. The close command flagged this row as "reached" rather than a named overlay member since I never added it explicitly with `overlay add` — worth doing next time to keep the working set accurate, though the close still succeeded and recorded the source correctly.
