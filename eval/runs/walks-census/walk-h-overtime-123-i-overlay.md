1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "A saturday, six hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day/hours/place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-legend-revision "warns overtime rate has three versions - need to confirm which applies to today 2026-09-21" --member /v1/nodes/sec-overtime-and-hours "map of how overtime hours are requested/logged/capped, may hold rounding rule"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_72ab0d --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body

2. **Answer**: Multiplier 2.01x; minutes rounded to the nearest 15 minutes. (This is the row for Saturday = day D2, six hours = hours H3, from home = place P4, in the current overtime table, in force since 2026-01-01, which covers today 2026-09-21.)

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (Saturday → D2)
- /v1/nodes/hard-overtime-legend-hours/body (six hours → H3)
- /v1/nodes/hard-overtime-legend-place/body (from home → P4)
- /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body (the multiplier and rounding figures)

4. **Notes**: The overtime table is coded (D#/H#/P#) rather than plain-language, so the real work was three legend lookups before the actual data row could be addressed — trying to guess a row address without reading all three legends first would have been a mistake. I also opened `sec-hard-overtime` as an overlay member expecting to read it directly, but it turned out to be a table listing the legends and ~64 individual per-combination row files rather than a single document; the legends and target row had to be read one by one. There is a legend-revision file warning of three historical versions of this rate table (superseded 2024-07-01–2025-12-31, and an older one before that); I didn't end up needing to open it since the row I read already stated its own effective date (2026-01-01 onward) and confirmed it's the current version covering today. The closing overlay report flagged the four documents I used as "reached = answered from somewhere the overlay never named" — they were sub-addresses under the `sec-hard-overtime` member rather than members I'd explicitly added, which is expected but worth noting as a quirk of how the overlay tracks provenance.
