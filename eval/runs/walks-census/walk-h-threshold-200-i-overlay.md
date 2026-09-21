1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, about 700,000 won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount-based approval threshold and whether quotes/comparison required" --member /v1/regions/expense "business trip expense rules, whether corporate card/receipts apply to flights and hotels"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_cc938d --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body

2. **Answer**: The team lead signs it off. No competing quotes are required. (This row's delegation limit is 1,032 thousand KRW, and the request qualifies for term M1 "just the once", category C3 "flights and hotels", amount V1 "about 700,000 won".)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m1/body

4. **Notes**: "Flights and hotels" is not an obviously procurement-shaped question at first glance — it reads like a travel/expense question, so I loaded both /v1/regions/procurement and /v1/regions/expense into the working overlay. The actual answer lived entirely in procurement's approval-threshold table, not in expense; the expense-side rows (corporate card, travel expense, corporate travel agency) were never touched. The three legend files (category/amount/term) are the only place the plain-language phrases in the question map to the row codes (C3/V1/M1) — skipping them would make it impossible to pick the right row out of the 64 in the table, since the rows only carry codes, not descriptions. I also had to confirm the row is the current one in force (from 2026-01-01, table sec-hard-threshold, vs. the superseded hard-threshold-v2 and threshold-table versions flagged by hard-threshold-legend-revision) — today's date (2026-09-21) falls inside that window, so I did not open the superseded versions. One oddity: on overlay close, the four addresses I passed via --used were echoed back as "reached" rather than a plain confirmation, with a note that this label means "answered from somewhere the overlay never named" — I had only added the two region-level members at overlay create time and never ran overlay add for the specific file addresses before closing, so the tool logged them as reached-but-not-formally-added. Didn't affect the outcome, but worth knowing that closing with --used addresses that were never added as members still works, just gets tagged differently.
