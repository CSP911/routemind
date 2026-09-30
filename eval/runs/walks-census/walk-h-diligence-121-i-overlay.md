1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 300,000,000 contract, custom-spec goods: site visit required? how often is vendor file re-reviewed?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods - likely has site visit rule" --member /v1/nodes/sec-vendor-performance-and-renewal "vendor performance/renewal review - likely covers re-review frequency" --member /v1/nodes/hard-diligence-legend-revision "warns diligence has 3 versions, need to confirm which applies"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2743c9 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body

2. **Answer**
Yes, a site visit is required. The vendor's file is re-reviewed every 12 months.
(This is under the current supplier due diligence table, in force since 2026-01-01, for origin O2 = Stuttgart, value band W3 = three hundred million won, goods category K2 = made to our spec. Screening score required is 55 and financial statements for the last two years are also needed, though those weren't asked.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three diligence versions applies to today's date, 2026-09-20)
/v1/nodes/hard-diligence-legend-origin/body (Stuttgart → origin O2)
/v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3)
/v1/nodes/hard-diligence-legend-goods/body (made to our spec → goods K2)
/v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k2/body (the row itself: site visit yes, re-review interval every 12 months)

4. **Notes**
The procurement area table carries a loud warning that supplier due diligence has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward) and that reaching for the newest is wrong for anything dated before 2026-01-01. Today's date (2026-09-20) falls in the current window, so `sec-hard-diligence` was correct, but it was worth confirming explicitly via the legend-revision page rather than assuming "current" meant "current table" — the same trap the page describes for a 2025-dated question.

The three qualifiers (origin, value band, goods category) are each in their own legend page and the row address has to be hand-assembled from them (e.g. `hard-diligence-row-origin-o2-value-w3-goods-k2`) — none of the legends cross-reference each other, so all three had to be read separately before the address could be built. This is the one case in the whole walk where an address is constructed rather than copied verbatim from a table, but it's sanctioned: the legends explicitly say the row is "indexed by the value in the right-hand column," and the resulting address matched one already printed in the overlay's expansion of `sec-hard-diligence`, so it was cross-checked against a printed address rather than trusted blind.

I initially considered `sec-vendor-performance-and-renewal` (renewal/review cadence) as the source for "how often does their file get looked at again," but the due diligence row itself already carries a "Re-review interval" field, which is the more direct and specific answer — the performance/renewal pages are a related but separate process (contract-term renewal decisions, not the due-diligence refresh cycle) and were not needed.
