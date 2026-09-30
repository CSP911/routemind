1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O2, value W3, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "origin/value/goods codes and site visit + review frequency sound like procurement vendor due diligence rules"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_352dc8 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Screening score required: 55; financial statements: last two years — for context, not asked.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established today's date, 2026-09-20/21, falls under the current version, not the two superseded ones)
- /v1/nodes/sec-hard-diligence (the current supplier due diligence table, in force from 2026-01-01, indexed by origin/value/goods)
- /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body (the row matching O2/W3/K2, giving the site-visit and re-review answer)

4. **Notes**
There are three versions of the supplier due diligence subject (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) covering different date ranges, and the legend-revision page warns explicitly that the oldest version says nothing about being superseded — so grabbing the first plausible-looking table without checking dates would have silently given a stale answer. Today's date (2026-09-20/2026-09-21) falls after 2026-01-01, so `sec-hard-diligence` is correct, but this is exactly the kind of question where reaching for whichever table "looks current" without reading the legend first would be a mistake — the legend page even calls out that for a 2025-dated question the middle version is the trap most likely to be gotten wrong in either direction. The row address itself was unambiguous once the qualifiers (O2/W3/K2) were confirmed, so no legend lookups for the origin/value/goods definitions were needed beyond the table listing itself.
