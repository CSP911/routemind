1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body

2. **Answer**:
For category C4, amount V1, term M2 (current table, in force from 2026-01-01, applicable to today's date 2026-09-20): the team lead signs it off, and no competing quotes are required ("Competing quotes: none"). Delegation limit is 1,049 thousand KRW; working days to expect is 3.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (used to confirm which of the three threshold versions applies to today's date)
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body (the row with the actual figures)

4. **Notes**:
The procurement area has three superseded versions of the approval threshold table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns explicitly that the oldest version says nothing about being replaced — so grabbing the first "approval threshold" hit without checking dates would have been wrong. Today's date (2026-09-20) falls under the current table (2026-01-01 onwards), so `sec-hard-threshold` was correct, but this required a deliberate date check rather than just picking the newest-looking table. Once at the current table, the row address for C4/V1/M2 was printed directly and unambiguously — no legend lookups for category/amount/term codes were needed since the question already gave the codes (C4, V1, M2) rather than plain-language descriptions.
