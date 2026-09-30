1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Saturday, 11 hours, on standby at home: what multiplier applies, and what rounding for minutes?" --member /v1/nodes/sec-hard-overtime "current overtime rate table since 2026-01-01, by day/hours/place" --member /v1/nodes/hard-overtime-legend-revision/body "warns which version covers which dates"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_bfcf2c --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body

2. **Answer**: Multiplier 2.10x; rounding to the nearest 20 minutes. (This is the current table, in force since 2026-01-01, which covers today's date of 2026-09-21.)

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body

4. **Notes**: The three legends (day, hours, place) had to be resolved separately before the row address could even be constructed — Saturday → D2, eleven hours → H4 (an exact match, no need to round to nearest band), on standby at home → P3. Easy to mis-map "on standby at home" to P4 ("from home") since both mention home; the legend's distinct wording (standby vs. plain from-home) is the only thing that disambiguates them. Also had to consciously confirm I was reading the current (2026-01-01-onward) table and not one of the two superseded overtime-rate versions the region page and legend-revision node both warn about — the row address itself doesn't restate the effective date, only a footnote in the row body does, which is easy to skip past.
