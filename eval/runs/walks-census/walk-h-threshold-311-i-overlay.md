1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Dinner with a client, roughly 3 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/expense "client entertainment expense — signature/approval needed for dinner cost" --member /v1/regions/procurement "recurring annual spend — approval threshold by amount/term, and whether competitive quotes are required"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d22beb --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body

2. **Answer**
The department head signs it off, and yes — two competing quotes are required. (Delegation limit for this row is 5,053 thousand KRW; working days to expect: 6.) This is under the current approval threshold table, in force from 2026-01-01.

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body — maps "dinner with a client" to category C4
- /v1/nodes/hard-threshold-legend-amount/body — maps "roughly 3 million won" to amount V2
- /v1/nodes/hard-threshold-legend-term/body — maps "renewing every year" to term M2
- /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body — the row itself: department head signs, two competing quotes, 6 working days

4. **Notes**
The question maps cleanly onto the procurement approval-threshold table's three legends (category, amount, term) — each phrase in the question ("dinner with a client," "roughly 3 million won," "renewing every year") is an exact match to a legend row, so there was no ambiguity in picking C4/V2/M2. The only place I nearly went wrong was starting the overlay: I put both /v1/regions/expense and /v1/regions/procurement in as members since "client dinner" sounded like an expense-category question at first glance, but the actual answer (signer + quotes) lives entirely under procurement's approval-threshold table, not expense. Worth noting the overlay's close output flagged all four addresses I used as "reached" rather than matched against named members — I had only added the two top-level region tables as members, not the specific leaf files I ultimately read, so the overlay didn't recognize them as pre-declared. The row itself carries a version note confirming it's in force from 2026-01-01 (current, since today is 2026-09-21) and superseded from `hard-threshold-v2` (2024-07-01 to 2025-12-31) and `threshold-table` before that — I did not need to open the legend-revision warning doc since the date match was unambiguous, but it's there if the "renewing every year" commitment had started under an older regime.
