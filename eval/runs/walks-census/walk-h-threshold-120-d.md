1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body

2. **Answer**: For category C2, amount V3, term M1 (delegation limit 20,024 thousand KRW, current table in force from 2026-01-01): the department head signs it off. Yes — three competing quotes are required before this can go through.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three versions is current for today, 2026-09-20)
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body (the answer itself)

4. **Notes**: The procurement table flags up front that the approval-threshold subject has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) sitting side by side with no withdrawal notice on the old ones — the oldest doesn't even say it's been replaced. It would have been easy to grab the first C2/V3/M1 row I saw without checking which version applies. I deliberately read the legend-revision page first: today (2026-09-20) falls in the 2026-01-01-onwards range, so `sec-hard-threshold` is correct and matches the three-qualifier indexing the legend describes. The row itself answered both halves of the question directly (signer + quote count), so no second document was needed for "other prices."
