1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4/body

2. Answer
Yes, a site visit is required. The file is re-reviewed every 6 months.

3. Source
/v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4/body

4. Notes
The procurement table lists three versions of the supplier due-diligence rules (a "legend-revision" warning node, `hard-diligence-v2`, and the current `sec-hard-diligence` table), which could easily lead to pulling numbers from a superseded version. The current table's own body states it has been in force since 2026-01-01, and today (2026-09-20) falls after that date, so `sec-hard-diligence` is the right one — I didn't need to open the superseded `hard-diligence-v2` or the legend-revision node, but it was tempting given how prominently the warning was surfaced in the table listing. The question already gave the row coordinates as exact codes (O2, W4, K4) matching the address scheme directly, so the origin/value/goods legends were not needed to translate a description into codes — I skipped reading them since the codes were already given, not derived from a job title, city, or amount that would need mapping.
