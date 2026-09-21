1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V3, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term lives here"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_06ab56 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body

2. **Answer**: For category C1, amount V3, term M1: the department head signs it off, and yes — three competing quotes are required before the purchase (delegation limit 20008 thousand KRW; 8 working days to expect).

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies to today's date)
- /v1/nodes/sec-hard-threshold (current threshold table, in force from 2026-01-01, indexed by category/amount/term)
- /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m1/body (the actual row with signer and quote count)

4. **Notes**: The approval threshold subject has three versions in force over different date ranges, and the legend page warns explicitly that "the oldest says nothing at all about having been replaced" — so grabbing the first hit under a name like `hard-threshold-v2` or assuming the newest table always applies would be wrong for an older question. Today's date (2026-09-21) falls cleanly inside the current table's range (2026-01-01 onward), so this case was not the tricky one the legend calls out (that would be a question dated in 2025, which needs the middle version, `hard-threshold-v2`), but it was still worth checking explicitly rather than assuming. Once on the current table, the row address was a direct, unambiguous match for C1/V3/M1 — no legend lookups for the category/amount/term codes were needed since the question already gave them in the table's own notation.
