1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k2/body

2. **Answer**: No, a site visit is not required. The file is re-reviewed every 36 months. (For reference: screening score required is 47, financial statements not required.)

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (confirmed which version applies for today's date)
/v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k2/body (the row with the answer)

4. **Notes**: The procurement table warns up front that supplier due diligence has been written three times, with different in-force date ranges, and that "the oldest says nothing at all about having been replaced" — so grabbing the first due-diligence table seen without checking dates would have been wrong. Checked the legend-revision page first to confirm that for today (2026-09-20) the current table (`sec-hard-diligence`, in force from 2026-01-01) is the right one, not `hard-diligence-v2` or the original `supplier-due-diligence`. Once on the current table, the row for O2/W1/K2 was listed directly by address, so no legend lookups for origin/value/goods codes were needed since the codes were already given in the question.
