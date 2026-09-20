1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body

2. **Answer**
Accrues 1.38 days of leave per month. The carry-over limit is 5 days — that is the most that can still be held into January.
(This assumes "partner firm" = type E4, "eight months" = tenure T1, "Busan branch" = site L2, per the legends. Figures are from the table in force since 2026-01-01, which applies to today's date, 2026-09-20.)

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body

4. **Notes**
The attendance area lists three different leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no indication from their names alone which is current — the legend-revision page is what actually resolves this by date, and it explicitly warns that the oldest version doesn't announce its own replacement. Easy to grab the wrong one if you skip that page. Also, "how much off can I still be holding in January" reads at first like a request for a different document (e.g. a carryover/expiry policy elsewhere in the attendance area), but the row itself already contains a "Carry-over limit" field, so no second lookup was needed — it's just a second question answered by the same row. The row also warns that any carried-over excess beyond the limit, if not pre-approved, is settled at the stated figure and not recoverable, but that's a caveat rather than part of what was asked, so I left it out of the answer proper.
