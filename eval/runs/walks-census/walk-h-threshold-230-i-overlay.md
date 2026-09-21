1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, about 40 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/expense "trip covers flights/hotels, may define approval and quote requirements for travel expenses" --member /v1/regions/procurement "approval threshold by amount and category may require competitive quotes for large one-time purchases" --member /v1/regions/approval "whose signature/approval chain for this amount"
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_c4251f --outcome answered --used /v1/nodes/hard-moved-threshold/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body

2. **Answer**: The department head signs it off. Yes, other prices are required first: three competing quotes and a written comparison. (This row's delegation limit is 100,044 thousand KRW; expect 11 working days.)

3. **Source**:
/v1/nodes/hard-moved-threshold/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body

4. **Notes**: My first overlay pulled in members from /v1/regions/expense, /v1/regions/procurement, and /v1/regions/approval, since "flights and hotels" plausibly lives under travel expense policy rather than the general procurement threshold table. The near-miss: /v1/regions/approval's own table has a big warning node (hard-moved-threshold) saying spend approval thresholds moved entirely to procurement's sec-hard-threshold as of 2026-01-01 — the approval region's own approval-line/sec-approvals-that-move-money pages are stale for anything dated after that, and today (2026-09-21) is after it. Missing that warning would have led to citing the wrong (superseded) chain-of-signature page. The threshold table itself is indexed only by three legend-translated codes (category/amount/term), not free text, so "flights and hotels" / "about 40 million won" / "just the once" each had to be looked up in a separate legend file before the row address could be built — the table listing alone (64 rows, C1-C4 × V1-V4 × M1-M4) gives no way to pick the right row without those three lookups. Note the amount legend's wording is inexact: "about 40 million won" maps to V4, whose banded label is also "about 40 million won" (delegation limit 100,044 thousand KRW, i.e. ~100M) — the band ceiling is much higher than the label suggests, but it's still the correct nearest-match band per the legend's own instructions.
