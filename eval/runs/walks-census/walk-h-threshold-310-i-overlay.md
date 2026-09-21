1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Dinner with a client, roughly 3 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/expense "client dinner is likely entertainment expense; need approval threshold" --member /v1/regions/procurement "competitive quotes/prices requirement may live here"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d685d9 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**:
The team lead signs it off. Yes — two competing quotes are needed. (Delegation limit for this row is 5,052 thousand KRW, so a ~3 million won dinner is within the team lead's own authority; working days to expect: 5.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body

4. **Notes**:
"dinner with a client" is a literal entry in the category legend (→ category C4), "roughly 3 million won" is a literal entry in the amount legend (→ amount V2), and "just the once" is a literal entry in the term legend (→ term M1), so there was no judgment call or nearest-match reasoning needed — the question's wording was deliberately lifted straight from the legends. The one place I made sure not to skip: the threshold table has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page is explicit that reaching for the newest is wrong for a question dated before 2026-01-01. Today's date (2026-09-20/21) is safely inside the current table's in-force range, so `sec-hard-threshold` was correct, but I only trusted that after reading the revision legend rather than assuming "current" meant "latest." The initial overlay also pulled in the procurement region for "other prices," but the answer to that turned out to live inside the same threshold row (the "Competing quotes" column) rather than in a separate purchase-request/quotes document — worth flagging since it would have been easy to go hunting in procurement's `purchase-request` table for a quotes rule that isn't actually where this one is answered.
