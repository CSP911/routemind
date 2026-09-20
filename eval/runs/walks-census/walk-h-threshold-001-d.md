1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body

2. **Answer**: For category C1, amount V1, term M2 (delegation limit 1,001 thousand KRW): it is signed off by the team lead. Competing quotes required: none — so no, other prices do not have to be obtained first.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed the current, 2026-01-01-onward table is the right version for today's date, 2026-09-20)
- /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body (the row with the actual answer)

4. **Notes**: The procurement area has three superseded versions of the approval-threshold subject (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns the oldest version doesn't flag itself as replaced. Easy to grab the wrong one if you skip that check — today's date (2026-09-20) falls under the current table (`sec-hard-threshold`, in force from 2026-01-01), so no ambiguity here, but it's the kind of question where guessing "newest is always right" would coincidentally work today and fail on a 2025-dated question. The row itself was a direct, unambiguous hit — no need to consult the category/amount/term legends since the question already gave the codes (C1/V1/M2) verbatim rather than descriptions needing translation.
