1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A consultant's time, roughly 3 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "procurement table covers approval thresholds by category, amount, and term - matches recurring consulting service spend"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_b7769c --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body

2. **Answer**: The department head signs it off. Yes — two competing quotes are required. (Delegation limit for this row is 5,021 thousand KRW; expect 6 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three approval-threshold versions applies for today's date, 2026-09-21)
- /v1/nodes/hard-threshold-legend-category/body ("a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body ("roughly 3 million won" → amount V2)
- /v1/nodes/hard-threshold-legend-term/body ("renewing every year" → term M2)
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body (the row itself: signer, quotes required)

4. **Notes**: The approval threshold subject has three superseded/current versions covering different date ranges, and the legend-revision page warns explicitly that reaching for the newest version is wrong for anything dated before 2026-01-01. Today's date (2026-09-21) falls cleanly in the current table's range (2026-01-01 onward), so this wasn't actually a trap here — but it would have been easy to skip that check and just grab `sec-hard-threshold` without verifying the date, which happens to have been correct this time only by luck of the date given. The three legends (category, amount, term) all mapped the question's phrasing onto their codes with exact or near-exact wording matches ("a consultant's time" and "roughly 3 million won" and "renewing every year" all appeared verbatim in the legend tables), so no ambiguity in picking the row. No confusion otherwise.
