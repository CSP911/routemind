1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body

2. **Answer**:
For category C4, amount V1, term M1 (delegation limit 1,048 thousand KRW), the sign-off is the team lead. No, you do not have to get other prices first — competing quotes required: none. Expect 2 working days for this approval.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies given today's date, 2026-09-20/21, is after 2026-01-01)
- /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body (the row with the answer)

4. **Notes**:
The procurement region lists three superseded/current versions of the approval-threshold subject (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and a legend-revision page warns explicitly that reaching for the newest table is wrong for dates before 2026-01-01. Today's date is well past that cutover, so the current table (`sec-hard-threshold`) is correct, but this is the exact trap the walk warns about — a careless run could have grabbed the first-listed or most-recently-touched threshold file without checking the effective-date table. I did not need to open the category/amount/term legend files separately since the question already gave the codes (C4, V1, M1) directly and an exact-match row address existed in the table listing — going to the legends would have been unnecessary extra hops for this particular question.
