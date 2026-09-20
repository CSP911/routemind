1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body

2. **Answer**
For type E4, tenure T1, site L3 (current table, in force since 2026-01-01):
- Accrues 1.40 days per month.
- Carry-over limit is 6 days — that is the most that can still be held going into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed which version applies to today's date, 2026-09-20)
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body (the figures)

4. **Notes**
Leave accrual has three superseded versions (`leave-accrual`, `hard-accrual-v2`, and the current
`sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is
wrong for any question dated before 2026-01-01. Today's date (2026-09-20) falls inside the current
table's range, so no correction was needed here, but it would have been easy to skip that check and
grab the current table on reflex — worth confirming every time rather than assuming. The E4/T1/L3
row existed directly under the current table's listing with no legend lookup required, since the
question already gave type/tenure/site as codes rather than plain-language descriptions.
