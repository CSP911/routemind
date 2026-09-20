1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k2/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months. (Also on this row: screening score required 43; financial statements last three years, audited.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions is current for today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k2/body (the answer)

4. **Notes**
Supplier due diligence has three superseded versions of this table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page explicitly warns that the oldest version says nothing about being replaced — so grabbing the first "supplier due diligence" hit without checking versioning would silently give a stale answer. Today's date (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` (indexed by three qualifiers: origin, value, goods) applies. I detoured briefly through `/v1/nodes/sec-supplier-due-diligence` ("where to start") expecting it to point at the row table, but it only covers the four conceptual due-diligence pages (disqualification, sanctions/ownership, code of conduct, overview) — not the origin/value/goods matrix. That matrix lives directly under `/v1/nodes/sec-hard-diligence`, one level up. Once there, the row for O1/W4/K2 was listed explicitly by name, so no legend lookups for the O/W/K codes were needed.
