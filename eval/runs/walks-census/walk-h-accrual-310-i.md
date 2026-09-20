1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**
Accrues 1.44 days of leave per month. Carry-over limit (how much can still be held going into January) is 7 days.
(Row also notes: 5 working days' notice required to book leave, and this leave does not accrue during unpaid leave — not asked, but on the same row.)

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l1/body
/v1/nodes/hard-accrual-legend-revision/body (used to confirm the current table, effective 2026-01-01, is the correct version for today's date)

4. **Notes**
The type legend is a trap: "on a two-year contract" maps to E2, and the user separately said "been here two years" — it would be easy to conflate the two-year phrase with the two-year-contract row. But the user identified themselves as "here from our partner firm," which is its own row (E4), and "been here two years" is tenure (T2), a completely separate axis. Used the partner-firm wording for type and the two-years wording for tenure — they resolve to different codes (E4/T2), not the same one.
Also had to actively check the accrual-legend-revision page before trusting the current table, since RouteMind stores three superseded versions of this same subject and a 2025-dated question would need the middle version, not this one. Today's date (2026-09-20) falls in the current table's window (2026-01-01 onward), so `sec-hard-accrual` was correct, but this is easy to get wrong by grabbing the newest table without checking effective dates.
"How much can still be holding in January" was read as the row's "Carry-over limit" field — the row states this limit directly rather than as a separate rule elsewhere, so no further lookup was needed once the row was found.
