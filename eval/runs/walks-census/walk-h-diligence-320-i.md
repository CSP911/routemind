1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body

2. Answer
Yes, a site visit is required. The file is re-reviewed every 12 months. (Also: screening score required is 86, financial statements for the last two years must be collected.)

3. Source
/v1/nodes/hard-diligence-legend-revision/body (established 2026-09-20 falls under the current table, not the two superseded versions)
/v1/nodes/hard-diligence-legend-origin/body (Da Nang → O4)
/v1/nodes/hard-diligence-legend-value/body (three hundred million won → W3)
/v1/nodes/hard-diligence-legend-goods/body (just office consumables → K1)
/v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body (final answer: site visit yes, re-review every 12 months)

4. Notes
The main trap here is version confusion: /v1/regions/procurement lists three separate due-diligence documents (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no obvious flag on which is current unless you stop and read the legend-revision page first. That page is explicit that the oldest version says nothing about being superseded, so grabbing the first-listed or most literally-named "supplier-due-diligence" node would silently give a wrong, outdated answer. Since today's date (2026-09-20) falls after 2026-01-01, the current table `sec-hard-diligence` is the correct one — no ambiguity for this particular date, but it would have been a live risk for a 2025-dated question.

The three qualifiers (origin/value/goods) are each in separate legend files with no cross-references beyond "see the legends" — easy to miss one and guess a code instead of confirming it. All three mapped cleanly to exact table entries (Da Nang, three hundred million won, office consumables all appear verbatim), so no fuzzy nearest-match judgment was needed here.
