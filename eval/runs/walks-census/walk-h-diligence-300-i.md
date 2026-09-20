1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body

2. Answer
No, a site visit is not required. The supplier's file gets re-reviewed every 36 months.
(Also for reference: screening score required is 78, financial statements not required.)

3. Source
/v1/nodes/hard-diligence-legend-revision/body — confirms 2026-09-20 falls under the current (2026-01-01 onward) table, not the two superseded versions
/v1/nodes/hard-diligence-legend-origin/body — Da Nang → origin O4
/v1/nodes/hard-diligence-legend-value/body — eight million won → value W1
/v1/nodes/hard-diligence-legend-goods/body — just office consumables → goods K1
/v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body — the row itself, giving "Site visit: no" and "Re-review interval: every 36 months"

4. Notes
The area is deliberately booby-trapped for date confusion: /v1/regions/procurement lists three eras of the diligence rules (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) side by side with no obvious flag on which applies today, and a dedicated legend-revision page exists specifically because "the oldest says nothing at all about having been replaced" — i.e. reaching for the plain `supplier-due-diligence` page would silently give a superseded answer with no warning on the page itself. I checked that page before touching the actual diligence table, which confirmed 2026-09-20 is squarely in the current (2026-01-01+) regime, so no version confusion here — but it would be very easy to skip that step and grab the wrong row.

The other near-miss: `/v1/nodes/sec-supplier-due-diligence` (the "where to start" overview) lists four pages including the old `supplier-due-diligence/body` as one of its children, mixed in among sanctions/code-of-conduct/disqualification pages. That old page is a leftover from the pre-2024-07-01 regime, sitting one click away from the current-table entry point with nothing marking it as superseded on the table listing itself — only the legend-revision page and its own body text (not read here, since it wasn't needed) would flag it as stale.

All three qualifiers (origin, value, goods) landed on exact table entries with no rounding or "nearest entry" judgment calls needed — Da Nang, eight million won, and "just office consumables" are all listed verbatim in their respective legends.
