1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D2, hours H1, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime multipliers often documented under attendance rules" --member /v1/regions/payroll "overtime pay multiplier could be a payroll concept"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e2f998 --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body

2. **Answer**
Multiplier: 1.71x. Rounding: to the nearest 5 minutes.

3. **Source**
/v1/nodes/sec-hard-overtime (table listing) → /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body (the row itself, used)

4. **Notes**
The initial overlay members were the two whole regions (attendance, payroll) rather than specific
nodes, since the question's shape (day/hours/place multiplier) could plausibly sit in either. The
attendance region row list made it obvious fast: `sec-hard-overtime` is explicitly labeled "THE
CURRENT OVERTIME RATE TABLE, in force from 2026-01-01" and is indexed by day/hours/place codes,
which is an exact match for the question's D2/H1/P2 shape — no need to open the payroll candidates
at all. The one thing worth flagging: there's a `hard-overtime-legend-revision` warning that this
rate has THREE versions with different rules, and a payroll-side node
(`hard-moved-overtime`) saying overtime premiums moved out of payroll into attendance on
2026-01-01. Today's date (2026-09-20/21) is safely inside the current table's effective range, so
the older `hard-overtime-v2` (2024-07-01 to 2025-12-31) or the pre-that `overtime-rate-table`
were never in contention — but a walk on a different date, or one that grabbed the first
"overtime" hit without checking the effective-date banner, could easily have pulled the wrong
version's multiplier/rounding. The row address itself (`hard-overtime-row-day-d2-hours-h1-place-p2`)
was printed verbatim by the table, so no construction was needed once the table was open.
