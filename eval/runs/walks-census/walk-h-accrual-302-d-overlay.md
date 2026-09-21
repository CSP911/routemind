1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T1, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/holding cap by employee type, tenure, site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f86b26 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body

2. **Answer**
Accrues 1.40 days per month. Carry-over limit (what you can still be holding, e.g. into January) is 6 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body

4. **Notes**
There are three versions of the leave accrual rules (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each covering a different date range, and the legend-revision page warns explicitly that reaching for the newest is wrong for any question dated before 2026-01-01. Today is 2026-09-20/21, and the "how much can I still be holding in January" phrasing points at the carryover cap going into the next January, so the current table (`sec-hard-accrual`, in force from 2026-01-01) is the right one — but this is exactly the kind of question where grabbing the newest table without checking the date would coincidentally give the right answer for the wrong reason. Worth flagging: since E4/T1/L3 is a fixed triple, the table listed a single exact-match row (`hard-accrual-row-type-e4-tenure-t1-site-l3`) rather than requiring a legend lookup to translate free-text into codes, so no ambiguity there.
