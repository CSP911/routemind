1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body

2. **Answer**
Yes, a site visit to the supplier's premises is required. The file is re-reviewed every 12 months.
(Also on this row, though not asked: screening score required is 88, and financial statements for the last two years must be collected.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (300 million won → value W3)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
- /v1/nodes/hard-diligence-legend-revision/body (confirmed current table applies as of 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body (site visit: yes; re-review: every 12 months)

4. **Notes**
- The first two pages I opened (sec-supplier-due-diligence and supplier-due-diligence) describe the general onboarding due-diligence gate — sanctions/ownership, code of conduct, disqualification — and nearly looked like the answer, but neither mentions a site visit or a re-review cadence. That's a dead end for this specific question; the real answer lives one level down, in the origin/value/goods row table under /v1/regions/procurement, not under the "where to start" overview.
- The region table's own description was the tell that pointed to the right place: it explicitly says the procurement area holds "the supplier due diligence required by origin, contract value and what is supplied," which matches the three qualifiers in the question (Da Nang / 300M won / people's time) — worth reading the table description closely before diving into subpages.
- There are three historical versions of this due-diligence table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page is explicit that reaching for the newest one is wrong for a pre-2026 date. Today is 2026-09-20, so the current table (sec-hard-diligence) is correct here — but this is exactly the kind of question where grabbing the first "supplier due diligence" hit without checking the version legend would silently give the wrong row for a dated question.
- The value legend bands are exact matches to spoken amounts (eight million, sixty million, three hundred million, seven hundred million won), so "three hundred million won" mapped cleanly to W3 with no rounding judgment needed — no ambiguity there.
