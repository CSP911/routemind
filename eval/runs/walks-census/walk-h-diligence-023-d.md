1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k4/body

2. **Answer**: Yes, a site visit is required. The file (re-review) is looked at again every 12 months.

3. **Source**: /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k4/body (confirmed as the current, in-force version via /v1/nodes/hard-diligence-legend-revision/body, since today 2026-09-20 falls after the 2026-01-01 cutover to the current table `sec-hard-diligence`)

4. **Notes**: The near-miss here is version confusion — supplier due diligence has been written three times (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the procurement table lists all three side by side with the superseded ones still present and undated at a glance. The legend-revision page makes clear the date decides which applies, and for 2026-09-20 that's unambiguously the current table. Also worth flagging: the row document's "If the figures are exceeded" section talks about excess amounts, budget holders, and recoverability — boilerplate that reads like it was copied from an expense/threshold-style page and doesn't actually pertain to site-visit or re-review-interval questions. It's easy to over-read that section as adding a condition to the site-visit requirement; it doesn't — the two answers (site visit: yes, re-review: every 12 months) are stated plainly in the table above it with no caveats.
