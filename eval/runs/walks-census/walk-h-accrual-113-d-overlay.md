1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T2, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual, monthly rate, and carryover/holding cap by employee type, tenure, and site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_dea59c --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body

2. **Answer**
For type E2, tenure T2, site L4: accrues 0.86 days per month, with a carry-over (holding) limit of 10 days. Today's date (2026-09-21) falls under the current accrual table (in force from 2026-01-01 onward), so this is the version that applies going into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body

4. **Notes**
This subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest one is wrong for dates before 2026-01-01. Since today is 2026-09-21, the current table (`sec-hard-accrual`, in force 2026-01-01 onward) was the right pick, but this is exactly the kind of question where grabbing a version without checking the in-force date would have silently given a stale answer — worth flagging even though it turned out to be the easy case here. The E2/T2/L4 row was an exact, unambiguous match for the question's three qualifiers, so no legend lookup for site/tenure/type codes was needed. The row's "carry-over limit" field is what I read as "how much can I still be holding" — the table doesn't use the word "holding," so that's an interpretive step, but carry-over limit is the only figure in the row that answers a question about how much banked leave can persist past year-end into January.
