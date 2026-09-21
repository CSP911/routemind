1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Ordinary Tuesday, ~90 min overtime from home: multiplier and minute rounding?" --member /v1/regions/attendance "overtime worked from home likely governed by attendance/time policy" --member /v1/regions/payroll "overtime multiplier and pay rounding likely defined in payroll policy"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_4f66b2 --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body

2. **Answer**: Multiplier 1.29x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/sec-hard-overtime (table listing, confirms this is the current overtime rate table in force from 2026-01-01)
- /v1/nodes/hard-overtime-legend-day/body ("an ordinary Tuesday" → day D1)
- /v1/nodes/hard-overtime-legend-hours/body ("about ninety minutes" → hours H1)
- /v1/nodes/hard-overtime-legend-place/body ("from home" → place P4)
- /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body (the row itself: multiplier 1.29x, rounding to the nearest 5 minutes)

4. **Notes**: The question's phrasing maps almost word-for-word onto the legend rows ("an ordinary Tuesday", "about ninety minutes", "from home"), which made the day/hours/place lookups unambiguous — no nearest-entry judgment call was needed. The one thing worth flagging: the attendance table carries a big WARNING that overtime rate has three historical versions (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime` from 2026-01-01), plus a note in payroll (`hard-moved-overtime`) that overtime premiums moved out of payroll into attendance as of 2026-01-01. Today's date (2026-09-20) falls inside the current version's window, so I used `sec-hard-overtime` and didn't need to touch the superseded `hard-overtime-v2`, but it would have been easy to grab a stale row if I hadn't checked the effective-date note on the row itself. Also worth noting: place P4 ("from home") is distinct from P3 ("on standby at home") — the question's "from home" phrasing matches P4 exactly, but the two are close enough in wording that a careless read could pick the wrong one.
