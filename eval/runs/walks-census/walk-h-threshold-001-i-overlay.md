1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "A couple of laptops, about 700,000 won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term - need signature level" --member /v1/nodes/hard-threshold-legend-revision "warns of three versions of threshold table, need to confirm which applies as of 2026-09-21" --member /v1/nodes/purchase-request "how many quotes are needed for a purchase"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_690b77 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body

2. **Answer**: The team lead signs it off. No competing quotes are required. This falls under category C1 (a couple of laptops), amount band V1 (about 700,000 won — delegation limit for this row is 1,001 thousand KRW), term M2 (renewing every year). Expect 3 working days.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m2/body

4. **Notes**: The procurement table for the threshold subject is a maze of three superseded versions plus a three-axis current table (4 categories × 4 amounts × 4 terms = 64 rows), so the real risk was reading the wrong version or misclassifying one of the three qualifiers. The legend-revision page settled the version question cleanly: today (2026-09-21) is well past 2026-01-01, so the current table `sec-hard-threshold` applies, not the two superseded ones — no ambiguity there, but it would have been easy to skip that check and just grab the newest-looking page without confirming the date rule. The three legend pages (category/amount/term) each mapped the plain-English question straight onto an exact row value (C1, V1, M2) with no "nearest entry" guessing needed, which was a relief given the legends' warning that mismatches require picking the nearest band and documenting it. I never actually opened `/v1/nodes/purchase-request` or `/v1/nodes/sec-hard-threshold` (the table) as sources — I added them to the overlay as candidates before knowing the row would answer the quotes question directly ("Competing quotes: none"), so they turned out to be unnecessary reads. The overlay's close output flagged the five addresses I used as "reached ... from somewhere the overlay never named" — that's just because I read row/legend body addresses directly rather than routing through the overlay table members I'd declared; the answer itself is unaffected.
