1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body

2. **Answer**
For category C1, amount V1, term M4 (current table, in force from 2026-01-01): the department head signs it off. No, other prices are not required first — competing quotes needed: none. (Delegation limit is 1003 thousand KRW; working days to expect: 5.)

3. **Source**
/v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body (also consulted /v1/nodes/hard-threshold-legend-revision/body to confirm the 2026-01-01-onwards table applies to today's date, 2026-09-20)

4. **Notes**
The procurement area holds three superseded versions of the approval-threshold table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the region/table listings don't say which one is current at a glance — the legend-revision page explicitly warns that "the oldest says nothing at all about having been replaced," so it would have been easy to grab a wrong-vintage row if the codes C1/V1/M4 happened to also exist in an older table without noticing the date. Confirming today's date (2026-09-20) fell in the "2026-01-01 onwards" band before reading the row was the one place this walk could have silently gone wrong. Otherwise the path was direct: the C1/V1/M4 row existed exactly as named in the table listing, so no legend lookups for category/amount/term codes were needed.
