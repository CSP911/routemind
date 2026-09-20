1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body

2. **Answer**:
For category C2, amount V3, term M2 (current table, in force from 2026-01-01, applicable to today's date 2026-09-21): the department head signs it off. Delegation limit is 20025 thousand KRW, and yes — three competing quotes are required before approval, with 9 working days to expect.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three versions applies to today's date)
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body (the actual figures)

4. **Notes**:
The procurement area warns up front that approval-threshold data has THREE superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and that the oldest version says nothing about being replaced — so grabbing the first plausible row without checking the legend-revision page would have silently returned stale figures. Today's date (2026-09-21) falls after the 2026-01-01 cutover, so the current table `sec-hard-threshold` was correct, but this was the exact trap the walk called out: assuming "newest is always right" or "oldest is always safe" are both wrong depending on the question's date. Once on the current table, the row address matched the C2/V3/M2 qualifiers exactly, so no legend lookups for category/amount/term codes were needed — the question already used the table's own coding scheme.
