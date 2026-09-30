1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two in the morning, about ninety minutes, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and rounding rules likely live in payroll" --member /v1/regions/attendance "standby/on-call time tracking may be defined in attendance"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_799eff --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body

2. **Answer**
Multiplier: 2.70x. Rounding: to the nearest 5 minutes.

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p3/body

4. **Notes**
The near-miss: the phrase "two in the morning" reads like a time-of-day/hours qualifier, but the day legend claims it, not the hours legend — "two in the morning" maps to day code D4, distinct from "an ordinary Tuesday" (D1), "a Saturday" (D2), or "Liberation Day" (D3). It would be easy to assume D4 means something like a night-shift day-of-week and instead try to force the clock time into the hours band. The hours band is driven purely by duration ("about ninety minutes" → H1), and the place band by the literal location phrase ("on standby at home" → P3, distinct from the highly similar "from home" → P4). All three legends state plainly they are the only place each mapping is written and to take the nearest entry if an exact match isn't listed, but here all three phrases in the question matched their legend rows verbatim, so no interpolation was needed.

One process note: the overlay's initial members were the two region tables (payroll, attendance), and I never called `overlay add` for the specific legend/row addresses as I narrowed in — I read them directly via `table`/`read` after finding them in the payroll/attendance table dump. The `overlay close` command accepted this but flagged each used address as "reached = answered from somewhere the overlay never named," i.e. addresses not tracked as formal working-set members. The outcome was still recorded as answered, but a cleaner walk would have run `overlay add` for `sec-hard-overtime` and the four leaf documents as they were identified, per the "narrow it as you learn more" instruction.

Also worth flagging for anyone re-running this: `/v1/nodes/hard-moved-overtime/body` under payroll warns overtime premiums moved to attendance as of 2026-01-01, and `sec-hard-overtime` under attendance is explicitly the current table in force from 2026-01-01 (today is 2026-09-20/21), so the current table was the correct one and the superseded `hard-overtime-v2` was correctly avoided.
