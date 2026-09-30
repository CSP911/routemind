1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H1, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime multipliers and rounding of minutes likely governed by attendance rules" --member /v1/regions/payroll "pay multipliers may be defined in payroll rules"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e3e4b5 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body

2. **Answer**
Multiplier: 1.23x. Rounding: to the nearest 5 minutes.

3. **Source**
/v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate versions applies to today's date)
/v1/nodes/sec-hard-overtime (current overtime rate table, in force from 2026-01-01, indexed by day/hours/place)
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body (the specific row with the multiplier and rounding)

4. **Notes**
Overtime rules turned out to live under /v1/regions/attendance, not payroll — a companion doc there (hard-moved-overtime) notes overtime premiums moved out of payroll into attendance on 2026-01-01, so the payroll member in my overlay was a dead end (payroll still had it before that date, but not now).

The trickier part was version selection: overtime rate has three superseded-but-not-marked-superseded versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision doc warns explicitly that "the oldest says nothing at all about having been replaced" and that grabbing the newest is wrong for any question dated before 2026-01-01. The question itself carries no date, but it's phrased with three qualifiers (day, hours, place), which per that same doc only the current table (`sec-hard-overtime`, in force from 2026-01-01) is indexed by — the two older versions use one and two qualifiers respectively. That, combined with today's date (2026-09-20) falling inside the current table's range, is what confirmed the current table was the right one rather than the v2 or original. Easy to have skipped that check and pulled the answer from the wrong version by reflex.
