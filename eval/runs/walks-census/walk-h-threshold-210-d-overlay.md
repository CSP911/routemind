1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay create --question "For category C3, amount V2, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table (2026-01-01 onwards), indexed by category/amount/term - directly matches C3/V2/M1 qualifiers" --member /v1/nodes/hard-threshold-legend-revision/body "confirms sec-hard-threshold is the correct version for today's date 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body
./bench/rmcli.py overlay add --id ov_2026-09-21_b980fb --address /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body --why "the exact matching row for C3/V2/M1 - answers signature and quotes question"
./bench/rmcli.py overlay close --id ov_2026-09-21_b980fb --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body

2. **Answer**: For category C3, amount V2, term M1: signs it off — the team lead. Yes, other prices are required first — two competing quotes. (Delegation limit 5036 thousand KRW; 5 working days to expect.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions is in force for today's date, 2026-09-21 → the current one)
- /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m1/body (the row with the actual figures: team lead signature, two competing quotes)

4. **Notes**: The approval threshold subject has three superseded/current versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page explicitly warns the oldest version says nothing about being replaced — it would be easy to grab the wrong one if a table just looked plausible. Checking the revision legend against today's date (2026-09-21, well past the 2026-01-01 cutover) before trusting `sec-hard-threshold` avoided that trap. Opening `sec-hard-threshold` expanded the overlay to all 64 category/amount/term row combinations plus three legend pages (amount banding, category definitions, term definitions) — the C3/V2/M1 row needed was already unambiguous from the question's own labels, so the legends for amount/category/term bands weren't needed to identify which row to read, only to know they exist if the qualifiers had been ambiguous.
