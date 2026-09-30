1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Liberation day, about ninety minutes, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table since 2026-01-01, likely has multiplier by day type/hours/place" --member /v1/nodes/sec-overtime-and-hours "overview of overtime and hours area, may cover rounding rules"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f46d27 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body

2. **Answer**: Multiplier 2.16x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Liberation Day → day D3)
- /v1/nodes/hard-overtime-legend-hours/body (about ninety minutes → hours H1)
- /v1/nodes/hard-overtime-legend-place/body (at my desk → place P1)
- /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body (multiplier 2.16x, rounding to the nearest 5 minutes)

4. **Notes**: The three qualifiers in the question (a named holiday, a duration, a location) each had to be translated through a separate legend file before the row address could be assembled — none of the legends repeat the mapping the others hold, and each says explicitly it is "the only place the mapping is written down," so skipping any one of them would have left a guess instead of a lookup. The overlay's "reached" note on close (rather than a straightforward match) is because I'd only added the two parent tables as members, not the individual legend/row files I actually read — those files were found by drilling into the tables I did add, not by naming them upfront in the overlay. Worth flagging: /v1/nodes/sec-overtime-and-hours also holds a file called overtime-rate-table, a differently-shaped description of overtime pay that sits alongside the hard-coded D/H/P row system; it's easy to grab that one by name and answer from the wrong table. I stayed with the sec-hard-overtime row system because its own table entry is explicitly labeled the current one (in force since 2026-01-01, which covers today, 2026-09-21), and the row I read confirms that in-force date range itself.
