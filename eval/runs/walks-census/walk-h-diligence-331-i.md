1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months. (Also required: screening score of 91, and audited financial statements for the last three years — not asked but part of the same row.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirms current table applies for dates from 2026-01-01, and today is 2026-09-20)
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → O4)
- /v1/nodes/hard-diligence-legend-value/body (700 million won → W4)
- /v1/nodes/hard-diligence-legend-goods/body ("something made to our spec" → K2)
- /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body (the answer: site visit yes, re-review every 6 months)

4. **Notes**: This subject has three superseded versions of the due-diligence table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page explicitly warns the oldest version says nothing about being replaced — an easy trap if you land on it directly via search rather than going through the legend-revision check first. Today's date (2026-09-20) falls cleanly in the current table's range (2026-01-01 onward) so there was no ambiguity here, but the check was necessary to be sure. The three qualifiers (origin/value/goods) are each a clean, exact match in their legends — "Da Nang" and "seven hundred million won" are listed verbatim, so no nearest-value judgment call was needed. The one place a wrong turn was plausible: "something made to our spec" could be misread as ambiguous between K2 and K3 ("people's time") if skimmed quickly, but the goods legend is explicit that custom-made goods are K2, not a service/labor category.
