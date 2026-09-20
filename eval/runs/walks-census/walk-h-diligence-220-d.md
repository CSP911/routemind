1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months.

3. **Source**: /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body

4. **Notes**: The procurement table lists three versions of supplier due diligence (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with an explicit warning that the newest is not always correct — a question dated in 2025 would need the middle (`hard-diligence-v2`) version instead. Checked the revision-legend page first to confirm which version applies: today's date (2026-09-20) falls under the current table (`sec-hard-diligence`, in force from 2026-01-01), so no ambiguity here, but it would have been easy to grab the current table reflexively without checking. The current table is indexed by exactly the three qualifiers given in the question (origin, value, goods), so the row address could be built directly from the table listing without needing the separate legend pages for origin/value/goods codes.
