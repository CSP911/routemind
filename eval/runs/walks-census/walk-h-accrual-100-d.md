1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**:
For type E2, tenure T1, site L1: accrues 0.72 days per month, with a carry-over limit of 4 days. So you can still be holding at most 4 days when carrying into January.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body
/v1/nodes/hard-accrual-legend-revision/body

4. **Notes**:
The accrual subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns that reaching for the newest is wrong for dates before 2026-01-01. This question wasn't dated in the past, and "January" here reads as upcoming (next accrual-year rollover), which still falls under the current table (in force from 2026-01-01, no end date given) — so `sec-hard-accrual` is the right version, but it was worth the extra check given the explicit warning about version mix-ups being the most common mistake in this area. The question's own codes (E2, T1, L1) matched the table's row-indexing scheme exactly, so no legend lookup for type/tenure/site definitions was needed to resolve ambiguity.
