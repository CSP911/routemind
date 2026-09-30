1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "A couple of laptops, roughly 3 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table - determines whose signature is needed by category/amount/term" --member /v1/nodes/purchase-request "purchase request process - how many quotes/other prices needed before approval"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_1d8e9a --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body

2. **Answer**: The department head signs it off. Yes — two competing quotes are needed before approval. (Delegation limit for this band is 5,005 thousand KRW; expect 6 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m2/body

4. **Notes**: The three qualifiers (category, amount, term) each had to be resolved through a separate legend before the right row could be picked — "a couple of laptops" maps to category C1, "roughly 3 million won" to amount V2, and "renewing every year" to term M2, giving row hard-threshold-row-category-c1-amount-v2-term-m2. It would be easy to miss that "renewing every year" is a *term* qualifier (annual commitment) rather than just an amount detail — the wording doesn't scream "term" the way "locked in for three years" does. Also worth flagging: the procurement table warned that the approval threshold has had three versions, and the row I used explicitly states it's in force from 2026-01-01, which covers today (2026-09-21), so no need to fall back to the superseded hard-threshold-v2 or threshold-table versions. I never opened the purchase-request table itself since the threshold row already answered the quotes question directly ("Competing quotes: two"), so that member ended up unused.
