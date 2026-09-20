1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2/body

2. **Answer**: For category C3, amount V1, term M2 (current table, in force from 2026-01-01): the team lead signs it off. No competing quotes are required ("Competing quotes: none"). Delegation limit is 1,033 thousand KRW; working days to expect is 3.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (to confirm which of the three threshold table versions is current for today's date)
- /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2/body (the answer)

4. **Notes**: The procurement table warns up front that the approval-threshold subject has THREE versions (old `threshold-table`, `hard-threshold-v2` for 2024-07-01–2025-12-31, and current `sec-hard-threshold` from 2026-01-01), and that the oldest version says nothing about being superseded — so picking a row without checking the legend-revision page first could silently give a stale answer. Today's date (2026-09-20/21) falls under the current table, so `sec-hard-threshold` was correct, but this is the kind of question where grabbing the first plausible row would have been wrong. The row itself directly named the signer and the quote requirement, so no further legend lookups (amount/category/term banding) were needed since the question already gave codes (C3, V1, M2) rather than plain-language amounts.
