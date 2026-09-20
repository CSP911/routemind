1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body

2. **Answer**:
Yes, a site visit is required. The file is re-reviewed every 6 months.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which version is current for today's date, 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body (the answer: Site visit = yes, Re-review interval = every 6 months)

4. **Notes**:
Supplier due diligence has three versions covering different date ranges, and the oldest version doesn't say anywhere that it's been superseded — so it would be easy to land on `supplier-due-diligence` (the oldest, no-warning page) and never know it was wrong. I checked the legend-revision page before trusting the current table, which confirmed 2026-09-20 falls under the current version (`sec-hard-diligence`, in force from 2026-01-01). The question already gave the codes (O3, W4, K2) directly rather than descriptive terms, so there was no need to consult the origin/value/goods legends to translate anything — the row address was assembled straight from the codes given and matched exactly.
