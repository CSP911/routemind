1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body

2. **Answer**: For type E2, tenure T3, site L3 (current table, in force from 2026-01-01): you accrue 0.92 days per month, and the carry-over limit is 12 days — that is the most you can still be holding going into January.

3. **Source**: /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body (also consulted /v1/nodes/hard-accrual-legend-revision/body to confirm today's date, 2026-09-20, falls under the current 2026-01-01-onward table rather than the superseded versions).

4. **Notes**: The attendance area lists three separate vintages of the accrual rules (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with an explicit warning that reaching for the newest one is wrong for dates before 2026-01-01. Since today is 2026-09-20, the current table (`sec-hard-accrual`) was the correct one, but it would have been easy to skip the legend-revision check and just grab whichever accrual page looked most complete. The row address itself encodes all three qualifiers (type/tenure/site) exactly as given in the question, so no legend lookups for site/tenure/type codes were needed. The "how much can I still be holding in January" phrasing maps directly onto the row's "Carry-over limit, days" field — nothing else in the row or table suggested a distinct, separate figure for January specifically.
