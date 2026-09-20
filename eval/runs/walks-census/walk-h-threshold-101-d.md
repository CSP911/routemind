1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body

2. **Answer**: For category C2, amount V1, term M2 (current table, in force from 2026-01-01, which applies since today is 2026-09-20): the delegation limit is 1017 thousand KRW, and it is signed off by the team lead. Competing quotes required: none — so no, you do not have to get other prices first.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three versions applies to today's date)
/v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body (the answer itself)

4. **Notes**: The procurement area flags up front that the approval threshold has three superseding versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) and warns that the oldest version says nothing about being replaced, so grabbing the first-looking match would silently give a stale answer. Checked the legend-revision page before reading any row, confirmed 2026-09-20 falls in the current (2026-01-01 onward) version, and only then read the C2/V1/M2 row from `sec-hard-threshold`. The question's codes (C2, V1, M2) matched the row's own qualifiers exactly, so the amount/category/term legend pages weren't needed to translate anything. The row's "Competing quotes: none" line directly answers the second half of the question — easy to miss if only skimming for the signer.
