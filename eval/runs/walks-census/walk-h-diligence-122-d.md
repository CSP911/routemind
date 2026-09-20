1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months. (Screening score required: 56; financial statements: last two years — supporting context, not directly asked.)

3. **Source**:
/v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body

4. **Notes**: The procurement area lists three versions of the due-diligence table (a "legend-revision" warning page, `hard-diligence-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-diligence` in force from 2026-01-01). Today is 2026-09-20, so the current table is correct and I didn't need to open the superseded `hard-diligence-v2` or the revision-legend page — but it would be easy to grab the wrong version if working from an older bookmark or not checking today's date against the "in force from" line. I detoured through `/v1/nodes/sec-supplier-due-diligence` (the "where to start" overview of four due-diligence pages: sanctions/ownership, code of conduct, disqualification triggers, and ongoing re-checks) expecting it might hold the site-visit/re-review cadence, but that page only describes the general due-diligence process, not the per-row figures — the actual numbers live in the row table under `sec-hard-diligence`, indexed directly by origin/value/goods codes matching exactly what was asked (O2/W3/K3), so no legend lookup was needed to translate the codes.
