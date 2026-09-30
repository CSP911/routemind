1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C2, amount V2, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term, in force since 2026-01-01" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold table has three versions - need to confirm which is current for today's date"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_7276c0 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m1/body

2. **Answer**: The team lead signs it off. Yes — two competing quotes are required before this can go through. (Delegation limit for this row is 5020 thousand KRW; working days to expect is 5.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed today's date, 2026-09-21, falls under the current table, not the two superseded versions)
/v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m1/body (the row itself: signer, quotes, limit, turnaround)

4. **Notes**: The threshold table has three superseded/current versions indexed by date, with an explicit warning page saying the oldest version does not admit it's been replaced — reaching for the newest version without checking date would be wrong for a question dated before 2026-01-01. Here the date (2026-09-21) is safely inside the current table's range (2026-01-01 onward), so this wasn't a live trap, but it was worth confirming rather than assuming. The overlay's member list surfaced the exact row address (three qualifiers: category/amount/term) directly without needing to open the category/amount/term legend pages, since C2, V2, and M1 in the question matched the table's own qualifier codes literally — no interpretation needed. One quirk: the overlay close reported the row address as "reached" rather than a matched member, since I'd only added the parent table and the legend page as members, not the individual row — harmless, but worth noting for how the overlay tracks provenance.