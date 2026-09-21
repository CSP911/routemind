1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C2, amount V3, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches the question directly"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_712e3a --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body

2. **Answer**:
For category C2, amount V3, term M2 (delegation limit 20,025 thousand KRW): the department head signs it off, and yes — three competing quotes are required before it goes through. Working days to expect: 9.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions is current as of 2026-09-21)
- /v1/nodes/sec-hard-threshold (the current table's index, listing the row for C2/V3/M2)
- /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body (the actual figures: signer, quotes required, delegation limit, working days)

4. **Notes**:
The approval threshold subject has three superseded/current versions in force over different date ranges, and the legend page is explicit that "the oldest says nothing at all about having been replaced" — so grabbing the first plausible-looking table without checking the legend-revision page first would have been a real risk of returning stale figures. Today's date (2026-09-21) falls after the 2026-01-01 cutover, so the current table (`sec-hard-threshold`) was correct, but this is exactly the kind of question where reaching for the newest-looking node without checking the date range is the trap the legend page warns about. Once on the current table, the row address was constructed by the tool's own listing (category-c2-amount-v3-term-m2), not guessed — the index page lists all 64 rows explicitly with the exact category/amount/term combination in the address, so no legend lookups for amount/category/term codes were needed since the question already gave the codes directly (C2, V3, M2).
