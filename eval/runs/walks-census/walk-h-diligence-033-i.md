1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body

2. **Answer**:
Yes, a site visit is required. The file is re-reviewed every 6 months.
(For reference, this row also requires a screening score of 45 and audited financial statements for the last three years.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions is current for today's date, 2026-09-20)
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → O1)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → W4)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → K4)
- /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k4/body (the answer: site visit yes, re-review every 6 months)

4. **Notes**:
The trap here is that supplier due diligence has three superseded versions living side by side (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the oldest one gives no indication it's been replaced — the legend-revision page explicitly warns that grabbing the newest table by reflex, or the oldest because it looks self-contained, are both wrong depending on the question's date. Since today is 2026-09-20, the current table (`sec-hard-diligence`, in force since 2026-01-01) was the correct one, but I checked the revision legend before committing to that pick rather than assuming.

The other near-miss: `/v1/nodes/sec-supplier-due-diligence` (the "where to start" overview) lists four due-diligence pages (disqualification triggers, sanctions/ownership checks, code of conduct, and the old `supplier-due-diligence` page) but does NOT list `sec-hard-diligence`, the actual current lookup table with the site-visit/re-review figures. If I'd stopped at that overview page I'd have missed the real answer entirely — the current three-qualifier table is filed directly under the procurement region table, not under this "where to start" node. Had to go back up to `/v1/regions/procurement` to find it.

Row selection itself was straightforward once the three legends (origin/value/goods) were read — Daejeon, 700M won, and "a licence" mapped cleanly to O1/W4/K4 with no ambiguity or nearest-match judgment calls needed.
