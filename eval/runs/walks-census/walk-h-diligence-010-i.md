1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months.
(Screening score required: 34; financial statements: last year — for context, not asked.)
This is under the current supplier due diligence table, in force since 2026-01-01, which covers today (2026-09-20).

3. **Source**
/v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
/v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
/v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
/v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body (site visit: no; re-review interval: every 24 months)

4. **Notes**
- All three inputs (Daejeon, sixty million won, office consumables) matched a legend row exactly — no nearest-neighbor guessing was needed, which is the case where this walk could easily go wrong.
- The procurement table listed both a current due-diligence table (`sec-hard-diligence`) and two superseded versions (`hard-diligence-v2`, plus a legend-revision warning page) sitting at the same level. It would be easy to grab a superseded row by accident. I confirmed via the row body's own footer ("In force from 2026-01-01") that this matches today's date before trusting the answer, rather than trusting the table title alone.
- I detoured through `/v1/nodes/sec-supplier-due-diligence` and its overview body first, expecting it to state the site-visit/re-review answer directly — it only gave a general narrative about the four due-diligence pages and didn't contain the figures. The actual answer only lives in the specific origin/value/goods row, not in any of the overview pages. Worth going straight to the legends next time rather than reading the overview first.
