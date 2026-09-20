1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body

2. **Answer**
For type E3, tenure T1, site L2 (current table, in force since 2026-01-01):
- Accrues 1.06 days per month.
- Carry-over limit is 5 days — that is the most you can still be holding into January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body

4. **Notes**
The attendance area lists three versions of the leave accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each covering a different date range, with a warning that the oldest doesn't say it's been superseded. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so that's the one used — but it would have been easy to grab the oldest or wrong-dated version without checking the legend-revision page first. The E3/T1/L2 row was addressable directly from the table listing (64 rows indexed by type/tenure/site), so no legend lookups were needed since the question already gave the codes in the table's own vocabulary. "How much can I still be holding in January" maps to the row's "Carry-over limit, days" field, not the monthly accrual figure — the two are easy to conflate since both are just numbers in the same table, but they answer different halves of the question (rate of accumulation vs. cap on balance carried into the new year).
