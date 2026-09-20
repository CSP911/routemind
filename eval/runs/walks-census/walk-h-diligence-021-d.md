1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body

2. **Answer**
Yes, a site visit is required. The file (re-review) is looked at again every 12 months.

3. **Source**
/v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k2/body
(/v1/nodes/hard-diligence-legend-revision/body used to confirm the current table version applies to today's date)

4. **Notes**
The procurement region lists three overlapping versions of the supplier due-diligence table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns that the oldest version never says it was superseded — reaching for the newest without checking would have been fine here since today (2026-09-20) falls under the current table (in force from 2026-01-01), but for a question dated in 2025 the correct answer would have come from `hard-diligence-v2` instead. Worth flagging because it's an easy trap in general, even though it didn't bite on this particular date. Otherwise the walk was direct: the origin/value/goods codes given in the question (O1, W3, K2) matched the row address exactly, so no legend translation was needed.
