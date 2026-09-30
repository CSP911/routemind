1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, six hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "holiday work-from-home hours, overtime multiplier and rounding rules likely tracked here" --member /v1/regions/payroll "overtime multiplier and pay rounding rules could be a payroll policy"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_341cb1 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body

2. **Answer**: Multiplier 2.49x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body

4. **Notes**: The overtime rate table exists in three versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision page warns pointedly against reaching for the newest by reflex. Today's date (2026-09-21) falls after the current table's 2026-01-01 start, so `sec-hard-overtime` is correct here, but this is the kind of question where grabbing the current table without checking the in-force date would sometimes be wrong — worth double-checking every time, not just this once. The three qualifiers (day/hours/place) each needed their own legend to translate plain language into a row code: "Liberation Day" → D3, "six hours" → H3 (an exact match, not a nearest-below case), "from home" → P4. Easy to trip up on P3 ("on standby at home") vs P4 ("from home") since both mention home — the question's "from home" phrasing matches P4's wording exactly, not P3's.
