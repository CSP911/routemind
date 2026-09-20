1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months.
(For context, this row also requires a screening score of 82 and last year's financial statements.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed today's date, 2026-09-20, falls under the current table, not the two superseded versions)
/v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body (the answer)

4. **Notes**
The supplier due diligence subject has three versions in force over different date ranges, and a warning page (`hard-diligence-legend-revision`) explicitly says the oldest version does not announce that it was replaced — so grabbing the first due-diligence table found without checking dates would have been wrong. Today's date (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` applies; I checked the revision-legend page before trusting that. The current table's row-listing table conveniently already spells out full origin/value/goods combinations in each row's address (e.g. `hard-diligence-row-origin-o4-value-w2-goods-k1`), so no separate legend lookup for what "O4", "W2", "K1" mean was needed — the exact row was addressable directly from the table listing. Nothing else in the walk was ambiguous.
