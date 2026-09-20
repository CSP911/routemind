1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body

2. Answer
Yes, a site visit is required. The file is re-reviewed every 12 months. (For reference, screening score required is 71 and financial statements for the last two years are also required.)

3. Source
/v1/nodes/hard-diligence-legend-revision/body (confirmed current version applies as of 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k2/body

4. Notes
The procurement area lists three versions of the supplier due diligence table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and current from 2026-01-01), and a legend-revision page explicitly warns that the oldest version doesn't say it was superseded and that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls squarely in the current version's range, so `sec-hard-diligence` was correct, but it would have been easy to skip the revision check and just grab the first "due diligence" looking table without confirming which version applies. Once inside `sec-hard-diligence`, the row for origin O3/value W3/goods K2 was listed directly by name (no separate legend lookup needed since the qualifiers were already given as codes), so no ambiguity there.
