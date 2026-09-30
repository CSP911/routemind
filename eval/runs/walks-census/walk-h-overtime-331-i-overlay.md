1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "2am, eleven hours, out at a client's office: what overtime multiplier applies, and what rounding is used for minutes?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place - covers today's date 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a4d37c --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body

2. **Answer**
Multiplier: 3.03x. Minutes are rounded to the nearest 20 minutes.
(Row also notes: approval needed in advance, and it counts toward the monthly cap — not asked but adjacent to the figures.)

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body

4. **Notes**
The trap here is "two in the morning" — it reads like a time-of-day detail, not a "day type," so the instinct is to treat it as irrelevant to the D1–D4 axis and go hunting for a separate night-shift multiplier elsewhere. But the day legend (hard-overtime-legend-day) explicitly maps "two in the morning" to day D4 — in this table's scheme, "day type" folds in the night-hours case rather than keeping it as a separate axis. Missing that would send the walk looking for a "night" row that doesn't exist under this key, or force a guess between D1 (ordinary weekday) and something else. The hours and place mappings were unambiguous exact matches (eleven hours → H4, "out at a client's office" → P2), so the only real ambiguity was the day axis. Confirmed the row's effective-date note (in force from 2026-01-01) covers today (2026-09-21), so the superseded v2/older tables didn't need checking.
