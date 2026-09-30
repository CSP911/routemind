1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Flights and hotels, around 12 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - likely holds signature/approval level for this amount and recurring term" --member /v1/nodes/purchase-request "purchase request process - may cover quotes requirement" --member /v1/nodes/hard-threshold-legend-revision/body "warns of three threshold versions - need to confirm which is current for today's date"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_1de4d2 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body

2. **Answer**: The department head signs it off. Yes — three competing quotes are required. (Delegation limit for this row is 20,041 thousand KRW; expect 9 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body

4. **Notes**: The revision-legend warning mattered here — there are three versions of the approval threshold table (old, 2024-07-01 to 2025-12-31, and current from 2026-01-01), and with today dated 2026-09-21 it would have been easy to grab a stale row without checking that first. The three-qualifier row address has to be assembled from three separate legend lookups (category, amount, term) rather than searched by description — "flights and hotels" maps to category C3, "around 12 million won" maps to amount V3 (matches the question's wording almost verbatim, which was reassuring), and "renewing every year" maps to term M2. No ambiguity in the legend mappings themselves; the only risk was skipping the revision check and landing on `hard-threshold-v2` or the oldest `threshold-table` by mistake.
