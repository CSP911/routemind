1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k3/body (the answer: Site visit = yes, Re-review interval = every 6 months)

4. **Notes**: Supplier due diligence has three versions in force over different date ranges (until 2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onwards), and the legend page warns explicitly that the oldest version says nothing about being superseded — so reaching for the newest table without checking would happen to be right here (today is 2026-09-20, inside the current 2026-01-01-onwards window), but only by luck if the date weren't checked. Worth flagging: the procurement table also lists a `hard-threshold` set of versions (approval threshold) with the same three-version structure — easy to conflate with the diligence versions since the row and column layout looks identical, but that table answers a different question (approval amounts, not site visits/review cadence). Once inside `sec-hard-diligence`, the three-qualifier row address (origin-o2-value-w4-goods-k3) was already spelled out in the table listing, so no guessing was needed — a good example of not constructing an address, just recognizing the printed one that matched.
