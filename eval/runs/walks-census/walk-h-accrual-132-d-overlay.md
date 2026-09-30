1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T4, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/holding cap likely live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9ae9e5 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body

2. **Answer**:
Under the current leave accrual table (in force from 2026-01-01, which applies since today is 2026-09-20/21), for type E2, tenure T4, site L3:
- Accrues 1.00 day per month.
- Carry-over limit (the most you can still be holding, e.g. into January) is 15 days.
(Also: 5 working days' notice required to take leave; does not accrue during unpaid leave.)

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body

4. **Notes**:
This subject has three superseded/current versions of the accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page explicitly warns the oldest version never announces it was replaced — reaching for the newest without checking is called out as wrong for pre-2026 dates. Since today's date (2026-09-20/21) falls in the current version's window, I used `sec-hard-accrual`, but this was the one place a careless walk could have grabbed the wrong table. The question conveniently supplied all three qualifiers (E2/T4/L3) as literal codes, so the row was a direct lookup in the 64-row table with no need to consult the site/tenure/type legend-translation docs. The overlay close output flagged both addresses I used as "reached ... from somewhere the overlay never named" since I hadn't formally added them as overlay members before closing — cosmetic, didn't affect the answer.
