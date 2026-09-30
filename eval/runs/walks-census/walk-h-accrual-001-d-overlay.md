1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T1, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carry-over/holding cap questions live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b974f3 --outcome answered --used /v1/nodes/sec-hard-accrual/body /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body

2. **Answer**
Accrues 0.42 days per month. Carry-over limit (the most that can be held/carried, e.g. into January) is 5 days.

3. **Source**
/v1/nodes/sec-hard-accrual/body (current leave accrual table, in force from 2026-01-01)
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body (the E1/T1/L2 row itself)

4. **Notes**
Leave accrual has three superseded/current versions with overlapping-looking names (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and a legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20/21) falls inside the current table's in-force window (2026-01-01 onward), so `sec-hard-accrual` is correct here — but this is exactly the kind of question where grabbing the first "accrual" hit without checking the revision-legend page would have risked pulling the superseded v2 figures instead. The row for E1/T1/L2 exists directly and unambiguously in the current table, so no legend lookups for type/tenure/site codes were needed.
