1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V2, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold table lives here by category/amount/term"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_2cd869 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body

2. **Answer**: The team lead signs it off, and yes — two competing quotes are required before it can go through. (Delegation limit for this row is 5004 thousand KRW; 5 working days to expect.)

3. **Source**: /v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies as of 2026-09-21), /v1/nodes/sec-hard-threshold (current table, listing the row for C1/V2/M1), /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m1/body (the answer).

4. **Notes**: The approval threshold subject has three versions in RouteMind (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page warns the oldest version never says it was superseded — so grabbing the first "approval threshold" hit without checking dates would silently give a stale answer. The question carried no date, so I used today's date (2026-09-21) against the legend to confirm `sec-hard-threshold` (in force from 2026-01-01) is correct, not `hard-threshold-v2` or the original `threshold-table`. Once on the current table, the row for C1/V2/M1 existed exactly as named — no ambiguity there, and the row itself answered both parts of the question directly (signer, and quote requirement) without needing a second document.
