1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (confirmed which version is in force for today's date)
/v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body (the answer)

4. **Notes**: The procurement table shows three separate diligence tables/pages (the oldest `supplier-due-diligence`, `hard-diligence-v2`, and the current `sec-hard-diligence`) each marked with different effective date ranges, and a legend page explicitly warns that grabbing the newest one is wrong for dates before 2026-01-01. Today (2026-09-20) falls under the current table, so `sec-hard-diligence` was correct, but this is an easy place to answer from a superseded row without noticing — the row addresses for the different versions aren't obviously distinguishable at a glance if you skip the legend check. Once in the current table, the row was addressed directly by the origin/value/goods codes given in the question, so no legend lookups for what O3/W4/K1 actually mean were needed.
