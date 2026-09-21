1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body
./bench/rmcli.py overlay create --question "For category C3, amount V2, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/hard-threshold-legend-revision/body "check which of the three threshold versions applies for today's date (2026-09-21)" --member /v1/nodes/sec-hard-threshold "current table (2026-01-01 onwards), indexed by category/amount/term — matches the date" --member /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body "the exact row for C3/V2/M2 — has signer and competing-quotes requirement"
./bench/rmcli.py overlay close --id ov_2026-09-21_743220 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body

2. **Answer**: For category C3, amount V2, term M2 (current table, in force 2026-01-01 onwards): the department head signs it off. Yes, other prices are required first — two competing quotes. Delegation limit is 5,037 thousand KRW, and 6 working days should be expected.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body

4. **Notes**: The near-miss here was the version trap. The procurement table lists three separate threshold documents (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) with an explicit warning page saying the oldest version never says it was superseded, so grabbing the first threshold-looking file without checking the legend would silently give a stale answer. Today's date (2026-09-21) falls in the current window (2026-01-01 onwards), so `sec-hard-threshold` was correct — but the warning explicitly calls out that a 2025-dated question needs the middle version instead, so this was worth confirming rather than assuming. Once in the current table, the three-qualifier addressing (category/amount/term) made the exact row (C3/V2/M2) a direct lookup with no ambiguity.
