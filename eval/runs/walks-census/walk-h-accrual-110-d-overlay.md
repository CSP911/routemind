1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T2, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/holding cap by type/tenure/site"
./bench/rmcli.py read /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5d0985 --outcome answered --used /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**
For type E2, tenure T2, site L1 (current table, in force from 2026-01-01):
- Accrues 0.80 days per month.
- Carry-over limit (the most that can be held at once, including into January): 7 days.

3. **Source**
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l1/body
/v1/nodes/hard-accrual-legend-revision/body

4. **Notes**
There are three versions of the leave accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each with different figures for the same type/tenure/site combination — grabbing the newest-looking one without checking dates would have been the wrong move for a question dated before 2026-01-01. I checked `hard-accrual-legend-revision`: today's date (2026-09-20/21) falls after 2026-01-01, so `sec-hard-accrual` is the correct, currently-in-force version and no version confusion applies here. The row for E2/T2/L1 exists verbatim under `sec-hard-accrual`, so no legend lookups (site/tenure/type) were needed to translate the codes — they were given directly in the question. The "how much can I still be holding in January" phrasing maps directly onto the row's "Carry-over limit" field; there is no separate January-specific figure in this table.
