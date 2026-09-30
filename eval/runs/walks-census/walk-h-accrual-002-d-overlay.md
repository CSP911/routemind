1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T1, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual and carryover rules likely live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_25e64d --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l3/body

2. **Answer**:
For type E1, tenure T1, site L3 (current table, in force from 2026-01-01, which covers today's date of 2026-09-20): accrues 0.44 days per month; the carry-over limit is 6 days — that is the most that can still be held/carried into January.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual table versions is in force for today's date)
- /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l3/body (the accrual rate and carry-over limit figures)

4. **Notes**:
This domain has three separate versions of the leave accrual rules (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each with the same E1/T1/L3-style row structure, and the legend-revision page explicitly warns that the oldest version says nothing about being superseded. It would have been easy to just grab the first accrual row that matched E1/T1/L3 without checking dates and get a stale figure. Checking the revision legend against today's date (2026-09-20, inside the 2026-01-01-onwards window) confirmed `sec-hard-accrual` was the right table before trusting its numbers. The question's phrasing "how much can I still be holding in January" maps onto the row's "carry-over limit" field — there was no separate January-specific rule, so I read the carry-over limit as the answer to that half of the question rather than searching further for a distinct "January" policy.
