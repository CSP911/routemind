1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Liberation day, eleven hours, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table in force from 2026-01-01, likely has multiplier by day type/hours/place" --member /v1/nodes/hard-overtime-legend-revision "warns which version covers which dates - need to confirm current version applies"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_445e30 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body

2. **Answer**: Multiplier 2.52x; rounding to the nearest 20 minutes. (This row is in force from 2026-01-01, still current as of today.)

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Liberation Day → day D3)
- /v1/nodes/hard-overtime-legend-hours/body (eleven hours → hours H4)
- /v1/nodes/hard-overtime-legend-place/body (at my desk → place P1)
- /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body (multiplier and rounding)

4. **Notes**: The overlay I created pointed at the current overtime table's member rows and a revision-legend page, but the actual work was in three separate legend pages (day, hours, place) that translate plain-language qualifiers into the D/H/P codes used to index the rate rows — those weren't in my initial overlay membership and had to be picked up from the /v1/regions/attendance table listing instead. Easy to go wrong here: "eleven hours" maps to H4 only because the hours legend bands by example ("about ninety minutes" / "three hours" / "six hours" / "eleven hours") rather than by numeric ranges, so a literal 11.0 vs 11.5 hours distinction doesn't matter — you match to the nearest listed example. Also worth flagging: the legend-revision file body came back empty when queried as a table member ("nothing here"), so the version-currency check was done by reading the "in force from 2026-01-01" note directly on the matched row instead — today's date (2026-09-21) is safely within that window.
