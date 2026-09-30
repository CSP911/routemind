1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, three hours, out at a client's office: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "holiday overtime pay multiplier likely defined here" --member /v1/regions/attendance "holiday work / overtime hours logging and rounding rules likely here"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_64677d --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body

2. **Answer**
Multiplier: 2.31x. Rounding: to the nearest 10 minutes.
(Row: day D3 = Liberation Day, hours H2 = three hours, place P2 = out at a client's office. Also requires approval in advance, and counts toward the monthly cap. Table in force from 2026-01-01, applicable to today's date of 2026-09-21.)

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body

4. **Notes**
Overtime pay used to live under payroll, but a warning node (/v1/nodes/hard-moved-overtime/body, surfaced by the initial overlay under the payroll region) says overtime premiums moved to attendance on 2026-01-01 — so the payroll region member of the overlay was a dead end and the real answer was entirely under attendance. The overtime table has three historical versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) each indexed differently, and the legend-revision doc is explicit that reaching for the newest is wrong for a question dated before 2026-01-01 — this question is dated 2026-09-21 (today), so the current three-qualifier table was correct, but it would have been an easy mistake to grab a version by habit without checking the date gate first. The three qualifiers (day/hours/place) are each translated through a separate legend doc that maps everyday phrasing to codes rather than the row table itself — "Liberation Day" → D3, "three hours" → H2, "out at a client's office" → P2 — and each legend explicitly says it is the only place the mapping is written down, so skipping straight to a row without reading all three legends risked guessing the code letters wrong.
