1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Liberation day, eleven hours, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table, in force since 2026-01-01, likely has the multiplier and rounding rule by day type/hours/place"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_53f423 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body

2. **Answer**: Multiplier 2.58x; rounding to the nearest 20 minutes. (Current table, in force from 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body
- /v1/nodes/hard-overtime-legend-hours/body
- /v1/nodes/hard-overtime-legend-place/body
- /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body

4. **Notes**: The overtime table isn't a flat table — it's indexed by three separate legends (day type, hour band, place category) that map plain-language descriptions to codes (D/H/P), and the actual rate lives in a row file addressed by the combination of all three codes. Creating the overlay on /v1/nodes/sec-hard-overtime auto-expanded to all 64 D×H×P row files plus the three legends, which made it obvious the legends had to be read first rather than guessing a row address. Each legend maps "Liberation Day" → D3, "eleven hours" → H4 (via the nearest-band rule, since eleven hours is the top band listed), and "on standby at home" → P3 (distinct from plain "from home," P4 — easy to conflate the two if skimmed quickly, since both are home-based). No ambiguity in the final row once the codes were resolved; the only real risk was picking P4 instead of P3 by not reading the place legend closely enough.
