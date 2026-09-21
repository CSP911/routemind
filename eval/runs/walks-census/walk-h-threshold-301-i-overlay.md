1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/corp-card
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body
./bench/rmcli.py overlay create --question "Dinner with a client, about 700,000 won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term" --member /v1/nodes/hard-threshold-legend-category "maps 'dinner with a client' to a category code" --member /v1/nodes/hard-threshold-legend-amount "maps 'about 700,000 won' to an amount code" --member /v1/nodes/hard-threshold-legend-term "maps 'renewing every year' to a term code"
./bench/rmcli.py overlay close --id ov_2026-09-21_fc6d9d --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body

2. **Answer**: The team lead signs it off, and no competing quotes are needed. This falls under category C4 ("dinner with a client"), amount band V1 ("about 700,000 won"), term M2 ("renewing every year") in the current approval threshold table (in force since 2026-01-01). The delegation limit for this row is 1,049 thousand KRW, and the working-day turnaround to expect is 3 days.

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body

4. **Notes**: My first instinct was to read this as an expense/entertainment question (a client dinner) and go looking in /v1/regions/expense for an "entertainment cap," which does exist there but doesn't answer "whose signature" or "other prices first" — those are procurement-threshold concepts (signer, competing quotes), not expense-cap concepts. The word "renewing every year" was the tell that this is really a procurement-threshold lookup: the current threshold table is indexed by category × amount × term, and "term" only makes sense for a recurring commitment, not a one-off meal. Once in /v1/regions/procurement, the three legend files gave exact, unambiguous matches (no "nearest entry" judgment calls needed): "dinner with a client" → C4 exactly, "about 700,000 won" → V1 exactly, "renewing every year" → M2 exactly, so the row category-c4-amount-v1-term-m2 was a clean pick with no guessing. One earlier wrong branch: I briefly opened /v1/nodes/corp-card looking for an entertainment-cap figure before realizing the question wasn't about card caps at all. Also worth flagging: the overlay's `close` output said the addresses I used were "reached ... answered from somewhere the overlay never named" — because I'd registered the legend files without their `/body` suffix and the row table as the whole `sec-hard-threshold` table rather than the single row file, so the exact strings didn't match what I ultimately cited as used. The content itself was correct either way, but it's a reminder that overlay members should be added with the exact final address you intend to cite, not just the parent/without-body variants.
