1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Flights and hotels, around 12 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term - need signature authority" --member /v1/nodes/purchase-request "how quotes work in a purchase request" --member /v1/nodes/hard-threshold-legend-revision/body "warning about three threshold versions, need to confirm which applies"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_28866e --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body

2. **Answer**: The division director must sign it off. Yes, three competing quotes are needed. (Delegation limit 20,043 thousand KRW; working days to expect: 11.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m4/body

4. **Notes**: Today's date (2026-09-21) matters a lot here — the revision-legend page warns that approval-threshold has three versions and the current one (sec-hard-threshold) only applies from 2026-01-01 onward; a 2025-dated question would need the middle version (hard-threshold-v2) instead, and the oldest version doesn't announce that it's been superseded. Easy to miss if you don't check that page first. The three qualifiers (category/amount/term) each have their own legend and none of the row pages repeat the plain-language description, so all three had to be resolved individually: "flights and hotels" → C3, "around 12 million won" → V3 (this one is a near-exact phrase match to the question, almost suspiciously convenient), and "until we cancel it" → M4 (also an exact phrase match). Once all three qualifiers were pinned down, the row address was assembled from the pattern shown in the procurement table listing rather than guessed. The purchase-request table member in the overlay ended up unused — the threshold row itself already answered both parts of the question (signer and quote count), so there was no need to open it.
