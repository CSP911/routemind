1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body

2. **Answer**: Yes, a site visit is required. The file (re-review) is looked at again every 12 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (confirmed which version is in force for today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body (the answer)

4. **Notes**: Supplier due diligence has three superseded versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls under the current table (`sec-hard-diligence`, in force from 2026-01-01), so no correction was needed here, but it would have been easy to skip that check and grab the wrong version by habit. The row address itself follows a predictable pattern (`hard-diligence-row-origin-o2-value-w3-goods-k2`), which matched the O2/W3/K2 qualifiers in the question directly once the table listing was seen — no legend lookups for origin/value/goods codes were needed since the question already gave the codes rather than descriptions.
