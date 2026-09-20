1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body

2. **Answer**
No site visit required. File is re-reviewed every 24 months.
(Screening score required: 50; Financial statements: last year — for context, not asked.)

3. **Source**
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body

4. **Notes**
The procurement area has two due-diligence tracks that look alike: a general "supplier-due-diligence"
narrative page (no site-visit/re-review figures, just the sanctions/code-of-conduct/disqualification
checks) and the actual figure table `sec-hard-diligence`, indexed by origin/value/goods codes. It would
be easy to stop at `supplier-due-diligence/body` and wrongly report "not found" since it has no numbers.
`sec-hard-diligence` also warns of THREE historical versions (legend-revision, v2, current) — had to
confirm this is the "in force from 2026-01-01" table, which matches today's date (2026-09-20), so no
need to chase the superseded `hard-diligence-v2`. All three legend lookups (Stuttgart→O2, sixty million
won→W2, office consumables→K1) were exact matches in their tables, not nearest-entry approximations, so
no rounding judgment call was needed here.
