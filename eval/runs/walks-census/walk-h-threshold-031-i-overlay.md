1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "A couple of laptops, about 40 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - likely has the signature/approval level for this amount and recurring term" --member /v1/nodes/hard-threshold-legend-revision "warns threshold table has three versions with different date ranges - need to confirm which applies to today 2026-09-21" --member /v1/nodes/purchase-request "purchase request process - how many quotes/prices needed before approval"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d36bc4 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m2/body

2. **Answer**
The division director signs it off. Yes, three competing quotes plus a written comparison are required before approval. (Delegation limit for this row: 100,013 thousand KRW; 12 working days to expect.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body (mapped "a couple of laptops" → category C1)
/v1/nodes/hard-threshold-legend-amount/body (mapped "about 40 million won" → amount V4)
/v1/nodes/hard-threshold-legend-term/body (mapped "renewing every year" → term M2)
/v1/nodes/hard-threshold-legend-revision/body (confirmed today, 2026-09-21, falls under the current table sec-hard-threshold, in force from 2026-01-01)
/v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m2/body (the row itself: signer, quotes, delegation limit)

4. **Notes**
The threshold table is indexed by three qualifiers (category, amount band, term) that are never spelled out on the row itself — each has to be looked up separately in its own legend page (hard-threshold-legend-category, -amount, -term) and translated into a code (C1/V4/M2) before the actual row address can be built from what the table printed. The phrase "about 40 million won" in the question matched the legend's own example wording for V4 almost verbatim, which made that one easy, but the other two ("a couple of laptops" → C1, "renewing every year" → M2) required reading full legend tables rather than guessing from the row list's truncated descriptions.

The real trap here was the revision warning: the procurement table flagged that approval-threshold has THREE versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward) covering the same subject at different addresses (threshold-table, hard-threshold-v2, sec-hard-threshold), and that the oldest version says nothing about being superseded — so grabbing the first/oldest-looking match would silently give a wrong, outdated answer. I deliberately fetched the legend-revision page before trusting sec-hard-threshold, and confirmed today's date (2026-09-21) falls in the "2026-01-01 onwards" band, which is the one the question's row-address family (three qualifiers, C1/V4/M2 naming) actually belongs to. Had this been a 2025-dated question, the correct source would have been hard-threshold-v2 instead, which does not use this row-naming scheme at all.
