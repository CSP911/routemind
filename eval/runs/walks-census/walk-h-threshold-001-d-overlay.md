1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V1, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term lives here"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_196808 --outcome answered --used /v1/nodes/sec-hard-threshold/body /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body

2. **Answer**: The team lead signs it off. No competing quotes are needed (Competing quotes: none). Delegation limit for this row is 1001 thousand KRW, with 3 working days to expect. This is the current table, in force from 2026-01-01.

3. **Source**:
/v1/nodes/sec-hard-threshold/body
/v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body

4. **Notes**: The procurement region table flagged that the approval-threshold document has THREE versions with a legend-revision warning — easy to grab a superseded one (`hard-threshold-v2`, in force 2024-07-01 to 2025-12-31) by mistake. I went straight for `sec-hard-threshold`, labeled as THE CURRENT table (in force from 2026-01-01), which matches today's date (2026-09-21), so no need to open the legend-revision page to disambiguate. The current table's row list is keyed directly by category/amount/term codes (e.g. `hard-threshold-row-category-c1-amount-v1-term-m2`), so once the right table was open the exact row was unambiguous — no need to consult the separate amount/category/term legend files since the question already gave codes (C1, V1, M2) rather than plain-language descriptions. One minor oddity: the overlay close command reported the two addresses I used as "reached" rather than as named members, since I navigated to them via `table`/`read` rather than adding them to the overlay with `overlay add` first — the answer is still correct, but the overlay's working set never formally tracked the final row.
