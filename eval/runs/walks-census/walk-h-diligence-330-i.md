1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months. (This is the current table, in force from 2026-01-01; today is 2026-09-20.)

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
/v1/nodes/hard-diligence-legend-value/body (700 million won → value W4)
/v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k1/body (site visit: yes; re-review interval: every 6 months)

4. **Notes**: All three lookup values (Da Nang, 700 million won, just office consumables) hit exact rows in their legends — no nearest-match guessing was needed, which is unusual given the legends' "if not listed, take the nearest entry" caveat. The main risk was going through the overview page (`sec-supplier-due-diligence`) first, which only describes the onboarding process narratively and does not contain the site-visit or re-review figures — those live only in the coded 64-row table (`sec-hard-diligence`) and require resolving all three legends first. Also had to consciously ignore the superseded versions (`hard-diligence-v2`, `supplier-due-diligence`) surfaced alongside the current table; the row itself confirms it's the version in force from 2026-01-01, which covers today's date.
