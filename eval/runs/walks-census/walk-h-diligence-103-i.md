1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body

2. **Answer**
No, a site visit is not required. The file is re-reviewed every 36 months.
(This is row origin O2 / value W1 / goods K4 — "a firm in Stuttgart" = O2, "eight million won" = W1, "a licence" = K4 — in the current supplier due diligence table, in force from 2026-01-01, which covers today's date of 2026-09-20.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → O2)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → W1)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → K4)
- /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body (site visit: no; re-review interval: every 36 months)

4. **Notes**
All three qualifiers in the question happened to be exact, unambiguous matches in their legends ("a firm in Stuttgart", "eight million won", "a licence" are verbatim rows) — no nearest-entry judgment call was needed, which is unusual and worth flagging since the legends explicitly warn you may have to pick the nearest entry if your case isn't listed.

The one place I paused was the version warning: the procurement table listed a `hard-diligence-legend-revision` node and a superseded `hard-diligence-v2` alongside the current `sec-hard-diligence` table, both under near-identical names ("Supplier due diligence"). I didn't open the legend-revision or v2 pages because the current table's own header states it's "in force from 2026-01-01" with no end date, and today (2026-09-20) falls inside that range — so the current table was the right one without needing to consult the revision legend. Worth double-checking in general, though: on a question closer to 2026-01-01 or if the date weren't given, skipping that legend could silently land on the wrong version.
