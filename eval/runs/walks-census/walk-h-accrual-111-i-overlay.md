1. Commands
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "On a two-year contract, been here two years, at the Busan branch: how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rates and carry-over/holding caps are attendance topics"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_105cc0 --outcome answered --used /v1/regions/attendance /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body

2. Answer
Accrues 0.82 days per month. Carry-over (holding) limit is 8 days. This is under the current leave accrual table, in force from 2026-01-01 (today is 2026-09-21, so this version applies).

3. Source
/v1/regions/attendance
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body

4. Notes
The three phrases in the question mapped cleanly onto the three legends with no ambiguity: "two-year contract" → type E2 (legend distinguishes this from "on the regular payroll" = E1), "been here two years" → tenure T2 (an exact match, not a nearest-band judgment call), and "Busan branch" → site L2 (also an exact match, distinct from "Seoul office" = L1). No fuzzy nearest-entry reasoning was needed anywhere.

The one place this could have gone wrong is the date/version trap: the legend-revision page warns that leave accrual has three versions and that reaching for the newest is wrong for any question dated before 2026-01-01. Today's date (2026-09-21, per the system reminder, one day after the task's stated "today") falls after the 2026-01-01 cutover, so the current table (`sec-hard-accrual`) is correct — but it would have been easy to skip that check and grab the current table on reflex without confirming the version actually covers the question's date. I checked the legend-revision page explicitly before reading the row.

"How much can I still be holding in January" reads most naturally as the general carry-over/holding cap (8 days) rather than a month-specific figure — the accrual table doesn't define a separate "January" rule, and there was no other row or note tying a cap specifically to January, so I treated "in January" as colloquial framing for "carried into the new year" rather than a distinct lookup.
