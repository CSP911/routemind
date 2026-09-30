1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, about ninety minutes, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and rounding rules likely live in payroll" --member /v1/regions/attendance "holiday work / time tracking rules likely live in attendance"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_5e121e --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body

2. **Answer**: Multiplier 2.25x; minutes rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body

4. **Notes**: The top-level regions table doesn't mention overtime by name, so the first guess (payroll vs. attendance) had to cover both — a warning node (`hard-moved-overtime`) confirms overtime premiums moved from payroll to attendance on 2026-01-01, so payroll would have been a dead end for anything current. The overtime table is a three-axis lookup (day × hours × place) resolved entirely through three separate legend documents rather than free text, so each qualifier in the question had to be translated individually: "Liberation Day" → day D3, "about ninety minutes" → hours H1 (matched verbatim against the legend's own wording), "from home" → place P4 (distinct from "on standby at home" = P3, which was the easy place to misread). There are also three historical versions of this table (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime` from 2026-01-01) — since today's date (2026-09-21) falls after the current version's start, the current table was the correct one, but it would have been easy to grab a superseded row if the legend-revision warning weren't checked. The overlay's close output flagged all four used addresses as "reached" rather than "used" because I never added them as explicit overlay members (only the two top-level region tables were members) — the answer is still correct, just narrowed by direct navigation rather than by editing the working set.
