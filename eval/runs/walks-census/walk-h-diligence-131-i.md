1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body

2. Answer: Yes, a site visit is required. The file is re-reviewed every 6 months.
(For completeness: this row also requires a screening score of 59 and audited financial statements for the last three years.)

3. Source:
- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → origin O2)
- /v1/nodes/hard-diligence-legend-value/body (seven hundred million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body (something made to our spec → goods K2)
- /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body (the answer: Site visit = yes, Re-review interval = every 6 months)
- /v1/nodes/hard-diligence-legend-revision/body (confirms today, 2026-09-20, falls under the current table, not a superseded one)

4. Notes:
- The first detour that nearly wasted time was /v1/nodes/supplier-due-diligence/body — it looked like the right generic "due diligence" doc (sanctions, code of conduct, disqualification screen) but it has nothing about site visits or review cadence. That content lives only in the origin/value/goods-indexed row table (sec-hard-diligence), not in the generic overview page.
- The procurement table lists three versions of the due-diligence rules (supplier-due-diligence, hard-diligence-v2, sec-hard-diligence) with near-identical names and overlapping subject matter — it would be easy to grab the superseded hard-diligence-v2 by mistake. I explicitly checked hard-diligence-legend-revision to confirm today's date (2026-09-20) falls in the "2026-01-01 onwards" current version, which matches sec-hard-diligence.
- The three legends (origin, value, goods) must each be resolved separately before the row address can be built — the row address itself is only assemblable after reading all three legends; guessing codes from the phrasing alone (e.g. assuming "Stuttgart" maps to some obvious O-number) would be wrong without checking the legend table.
