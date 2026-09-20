1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body

2. **Answer**: For type E4, tenure T3, site L3: accrues 1.56 days per month. Carry-over limit is 12 days — that is the most you can still be holding going into January.

3. **Source**: /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body (also consulted /v1/nodes/hard-accrual-legend-revision/body to confirm which version applies for today's date, 2026-09-20)

4. **Notes**: The attendance area's leave-accrual subject has three superseding versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly against reaching for the newest table without checking the date. Since today is 2026-09-20, the current table (`sec-hard-accrual`, in force from 2026-01-01) is the correct one — but this was worth pausing on, since a careless walk could have missed the version-legend page and just grabbed whatever table looked newest without confirming the effective-date range actually covers today. The question's "type E4, tenure T3, site L3" mapped directly onto the row address pattern (`hard-accrual-row-type-e4-tenure-t3-site-l3`), so no legend lookups for site/tenure/type codes were needed — the codes were already given verbatim. The "how much can I still be holding in January" phrasing isn't spelled out anywhere as a distinct figure; I read it as referring to the row's "Carry-over limit" field, which is the cap on days held past year-end.
