1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months. (For reference, this row also requires a screening score of 38 and financial statements for the last two years.)

3. **Source**: /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body — also consulted /v1/nodes/hard-diligence-legend-revision/body to confirm which version of the due-diligence table applies to today's date (2026-09-20).

4. **Notes**: This area has three superseded versions of the supplier due diligence table (pre-2024-07-01, 2024-07-01–2025-12-31, and current from 2026-01-01), and the legend page explicitly warns that grabbing the newest table is wrong for a question dated before 2026-01-01. Today's date (2026-09-20) falls cleanly in the current table's range (`sec-hard-diligence`), so there was no real ambiguity here, but it would have been easy to skip the version check and land on the wrong row entirely if the question had been dated in 2025. Once in the current table, the origin/value/goods qualifiers matched an exact row address, so no legend lookups for the O1/W3/K1 codes themselves were needed.
