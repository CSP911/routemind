1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Liberation day, eleven hours, out at a client's office: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day/hours/place since 2026-01-01" --member /v1/nodes/sec-overtime-and-hours "overview map of overtime rules, may contain rounding rule"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d7d90c --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body

2. **Answer**: Multiplier 2.55x. Rounding: to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p2/body

4. **Notes**: The question's three clauses map to the three legends exactly by their phrasing: "Liberation Day" appears verbatim in the day legend (→ D3), "eleven hours" appears verbatim in the hours legend (→ H4), and "out at a client's office" appears verbatim in the place legend (→ P2) — so this walk had no ambiguity once the legends were opened. The near-miss was upstream of that: the sec-hard-overtime table lists 64 individual row files (4 days × 4 hour bands × 4 places) with no obvious index, and it would be easy to guess a row address by pattern-matching the coordinates instead of reading each legend — the task explicitly forbids constructing addresses, and here it mattered, since without reading the legends I had no way to know eleven hours lands in the top hour band (H4) rather than some band literally named "11" or similar. I also note the overlay only had the two parent tables as members; the four file addresses I actually read were never added via `overlay add`, so the close command reported them as "reached" rather than as named/used members — worth calling out since it means the overlay's membership list understates what was actually consulted.
