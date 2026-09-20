1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k3/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k3/body (the answer: Site visit = yes, Re-review interval = every 12 months)

4. **Notes**
Procurement's table listing shows three due-diligence-related items side by side (`hard-diligence-legend-revision`, `hard-diligence-v2`, and the current `sec-hard-diligence`) with truncated descriptions — it would be easy to grab `hard-diligence-v2` by mistake since it sorts near the top and looks current at a glance. The legend-revision page makes clear there are three versions (pre-2024-07-01, 2024-07-01–2025-12-31 = `hard-diligence-v2`, and 2026-01-01 onward = `sec-hard-diligence`), and since today is 2026-09-20 the current table is the right one. Worth flagging: the legend explicitly warns that the oldest version says nothing about being superseded, so date-checking here is not optional. Once in `sec-hard-diligence`, the row for O3/W3/K3 existed directly and unambiguously — no interpolation needed.
