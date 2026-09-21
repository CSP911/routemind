1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon vendor, 700M KRW, labor/staffing category: is a site visit required, and how often is the vendor file reassessed?" --member /v1/regions/procurement "amount + category thresholds, site visit and re-review cadence likely live under procurement"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2acd94 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body

2. **Answer**
Yes, a site visit is required. The vendor's file is re-reviewed every 6 months. (This is the current supplier due-diligence table, in force from 2026-01-01; also requires a screening score of 44 and audited financial statements for the last three years.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
- /v1/nodes/hard-diligence-legend-value/body (700 million won → value W4)
- /v1/nodes/hard-diligence-legend-goods/body ("people's time" → goods K3)
- /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body (site visit: yes; re-review interval: every 6 months)

4. **Notes**
- My first instinct was to read `supplier-due-diligence/body` (the plain-named overview page, listed under `sec-supplier-due-diligence`), which describes three generic checks (sanctions/ownership, code of conduct, disqualification screen) but says nothing about site visits or amount/category-driven cadence — that page is not the answer and would have led to a wrong "not found" if I'd stopped there.
- The real table is `sec-hard-diligence`, reached only from `/v1/regions/procurement`, not from the `sec-supplier-due-diligence` overview branch — the two due-diligence trees look like they'd converge but don't.
- There is an explicit versioning trap here: `hard-diligence-legend-revision` warns of three versions of this table (`supplier-due-diligence`, superseded `hard-diligence-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-diligence` for 2026-01-01 onward). Today is 2026-09-20, so `sec-hard-diligence` is correct — but it would be easy to grab the superseded `hard-diligence-v2` by mistake since both live at similarly-named addresses.
- The three legends (origin, value, goods) must each be read separately to translate the plain-English question into the O1/W4/K3 row key — the row addresses give no hint which combination corresponds to "Daejeon, 700M won, people's time" without them.
- The overlay close command reported all four used addresses as "reached ... from somewhere the overlay never named" — I had only added `/v1/regions/procurement` as a member and drilled down manually rather than adding each intermediate address as a member; harmless here since the outcome was answered correctly, but worth noting for consistency in future walks.
