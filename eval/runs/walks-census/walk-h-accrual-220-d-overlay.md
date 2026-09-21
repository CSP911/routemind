1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T3, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "attendance covers leave accrual and balances"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c01237 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body

2. **Answer**: You accrue 1.20 days per month. The carry-over limit is 10 days, which is the most you can still be holding when the year turns over into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body

4. **Notes**: There are three versions of the accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each covering a different date range, and the legend-revision page warns explicitly that reaching for the newest one is wrong for anything dated before 2026-01-01. Today's date (2026-09-21) falls inside the current table's range (2026-01-01 onward), so `sec-hard-accrual` was the correct one to use — but this was the one place a walk could easily go wrong by grabbing the newest table out of habit without checking the date first. The question's phrasing "how much can I still be holding in January" doesn't name "carry-over limit" directly; I read it as asking for the cap on days carried into the new year, which is exactly the "Carry-over limit, days" field in the row. The row itself needed no legend lookup since the question already gave the three qualifiers (E3/T3/L1) as codes rather than descriptions.
