1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Vendor in Austin → origin O3; three hundred million won → value W3; something made to our spec → goods K2. Row O3/W3/K2 also requires a screening score of 71 and financial statements for the last two years, in force since 2026-01-01, which covers today's date of 2026-09-20.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body
- /v1/nodes/hard-diligence-legend-value/body
- /v1/nodes/hard-diligence-legend-goods/body
- /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body

4. **Notes**
The `/v1/regions/procurement` table lists a `hard-diligence-legend-revision` warning ("supplier due diligence has THREE versions") right next to the current table, which almost sent me down a rabbit hole of checking version-applicability dates before I noticed the current row itself states plainly "In force from 2026-01-01" — since today is 2026-09-20, that's unambiguous and the version-revision page didn't need to be opened.
The bigger risk was the initial detour through `/v1/nodes/sec-supplier-due-diligence` and `/v1/nodes/supplier-due-diligence` (the general "three checks" narrative pages about sanctions/code-of-conduct/disqualification) — these read as authoritative and on-topic but contain no site-visit or re-review-interval figures at all; the actual answer only lives in the 64-row lookup table (`sec-hard-diligence`), keyed by origin/value/goods codes defined in three separate legend pages. Someone answering from the narrative pages alone would wrongly report "not found."
Mapping the three inputs to codes was straightforward and each legend was unambiguous (Austin=O3, 300M won=W3, "something made to our spec"=K2) — no nearest-match guessing was needed.
