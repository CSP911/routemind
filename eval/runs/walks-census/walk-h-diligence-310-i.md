1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body

2. Answer
No, a site visit is not required. The file (screening) gets re-reviewed every 24 months.
(Also on this row, for context: screening score required is 82, and financial statements needed are "last year".)

3. Source
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
- /v1/nodes/hard-diligence-legend-goods/body (office consumables → goods K1)
- /v1/nodes/hard-diligence-legend-revision/body (confirms current table applies for 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body (the answer: site visit = no, re-review interval = every 24 months)

4. Notes
The main risk here was the versioning trap: supplier due diligence has three superseded versions (pre-2024-07-01, 2024-07-01–2025-12-31, and current from 2026-01-01), each at a different address and indexed by a different number of qualifiers. The legend-revision page explicitly warns not to reach for the newest reflexively — but today's date (2026-09-20) does fall under the current table (`sec-hard-diligence`), so that was the right pick, not a trap in this instance. Worth flagging that the walk relies on checking that revision page every time rather than assuming.

The other easy mistake would have been conflating this with the separate approval-threshold table (`sec-hard-threshold`), which lives right next to due diligence in the procurement region and answers a different question (how far up the amount needs sign-off, not whether a site visit is needed). The question here is purely about due diligence, so that table was never opened.

Mapping was clean and exact — "sixty million won" matched value band W2 verbatim, so no nearest-entry judgment call was needed for value, origin, or goods.
