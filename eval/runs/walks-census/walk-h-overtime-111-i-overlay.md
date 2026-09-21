1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A saturday, three hours, out at a client's office: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/weekend work hours likely tracked here" --member /v1/regions/payroll "overtime pay multiplier likely defined in payroll rules"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9623bd --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body

2. **Answer**: Multiplier 1.83x; minutes rounded to the nearest 10 minutes. (Current table, in force from 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body
- /v1/nodes/hard-overtime-legend-hours/body
- /v1/nodes/hard-overtime-legend-place/body
- /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body

4. **Notes**: The overlay I opened named only the two region tables (attendance, payroll); the actual answer lived several hops deeper under attendance, at `sec-hard-overtime`, so the overlay's own member list undersold where the answer was — I had to drill into the table's children manually rather than relying on the overlay rows themselves. The close command flagged all four addresses I used as "reached... from somewhere the overlay never named," which is expected since I never called `overlay add` for them individually; worth noting in case that's meant to be done for a stricter workflow. The three-qualifier lookup (day/hours/place → D/H/P codes) is easy to get wrong if you skip a legend: "a Saturday" maps to D2 (not D1, which is the ordinary-weekday code), "three hours" maps exactly to H2, and "out at a client's office" maps exactly to P2 — all three had exact matches in their legends, so no nearest-neighbor guessing was needed here, but the legends' "if not listed, take the nearest entry above it" caveat means a slightly different scenario (e.g. "two and a half hours") could have forced a judgment call. Also confirmed via `hard-overtime-legend-revision` context in the row body that this is the current (2026-01-01 onward) version, not one of the two superseded versions (`hard-overtime-v2`, `overtime-rate-table`) — worth checking explicitly since RouteMind has three overlapping versions of this table and today's date (2026-09-20) falls squarely in the current one.
