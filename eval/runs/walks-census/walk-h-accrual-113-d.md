1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body

2. **Answer**
For type E2, tenure T2, site L4 (current table, in force since 2026-01-01): accrues 0.86 days per month. Carry-over limit is 10 days — that is the most that can still be held in January (i.e. the cap on balance carried into the new year).

3. **Source**
/v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body

4. **Notes**
The area listing at /v1/regions/attendance flags up front that leave accrual has three superseded versions with different date ranges, and the legend-revision doc at /v1/nodes/hard-accrual-legend-revision/body warns explicitly that reaching for the newest table is wrong for any date before 2026-01-01. Since today is 2026-09-20, the current table (`sec-hard-accrual`, in force from 2026-01-01) is the right one, but this was the one spot where it would have been easy to grab the wrong version without checking. The question's E2/T2/L4 qualifiers mapped directly to one row in the 64-row table, so no legend lookup (type/tenure/site) was needed — the codes were already given in the question rather than needing translation from plain-language description. "How much can I still be holding in January" reads as the carry-over limit (10 days), not a separate January-specific figure — the row has no month-specific rule beyond that.
