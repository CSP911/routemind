1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "An ordinary tuesday, eleven hours, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers are typically payroll rules" --member /v1/regions/attendance "attendance covers work hours, overtime, and location-based work rules"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7e2e94 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body

2. **Answer**
Multiplier: 1.65x. Rounding: to the nearest 20 minutes.
(This is from the current overtime rate table, in force from 2026-01-01: day D1 = "an ordinary Tuesday", hours H4 = "eleven hours", place P4 = "from home".)

3. **Source**
- /v1/nodes/hard-overtime-legend-day/body
- /v1/nodes/hard-overtime-legend-hours/body
- /v1/nodes/hard-overtime-legend-place/body
- /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p4/body

4. **Notes**
The question phrases each qualifier in plain words on purpose, and the legend tables are the only place those words are mapped to the row codes ("ordinary Tuesday" → D1, "eleven hours" → H4, "from home" → P4) — you cannot guess the row address from the question text; you have to read all three legends first, then assemble `hard-overtime-row-day-d1-hours-h4-place-p4` from the codes. The main risk was picking the wrong table area at the first hop: overtime rates could plausibly live under payroll, but a warning node (`hard-moved-overtime`) surfaced in the payroll working set said overtime premiums moved to attendance on 2026-01-01, and the attendance region also carried three overtime-table versions (`hard-overtime-v2` superseded, `overtime-rate-table` older, and `sec-hard-overtime` current). Today's date (2026-09-20/21) falls after the 2026-01-01 effective date, so `sec-hard-overtime` is the correct current table — the superseded `hard-overtime-v2` row would have given a different multiplier/rounding pair if picked by mistake. The overlay close reported these four addresses as "reached" rather than formally tracked overlay members, since they were navigated to directly rather than added via `overlay add`; that's just a bookkeeping note, not a gap in sourcing.
