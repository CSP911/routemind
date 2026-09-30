1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon company, 300M won, licence: site visit required? review frequency?" --member /v1/regions/procurement "vendor diligence, thresholds, site visits, and review cadence likely live under procurement"
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_366352 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k4/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months. (This row also requires a screening score of 41 and financial statements for the last two years.) This is the current table, in force from 2026-01-01, which covers today's date.

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
/v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3)
/v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
/v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k4/body (the answer row)

4. **Notes**: The procurement table surfaced a scary warning up front — `hard-diligence-legend-revision` flags THREE versions of the supplier due diligence rules with overlapping-sounding names (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`). It would have been easy to grab the wrong one. I went with `sec-hard-diligence` because its own table header states plainly "THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-01-01," and the row itself confirms this front matter at the bottom, dating the row as current and naming the two prior versions superseded — so I never needed to open the revision-legend file itself. Today's date (2026-09-21) falls after 2026-01-01 with no listed end date, so this version applies cleanly with no ambiguity. The three legends (origin/value/goods) are straightforward one-to-one lookups; no rounding or nearest-match judgment calls were needed since Daejeon, 300M won, and "a licence" each hit an exact row in their respective legends. The overlay's `close` output flagged all four cited addresses as "reached" rather than "used somewhere the overlay named" — that's because the working set only listed the top-level `sec-hard-diligence` table, not its child legend/row files drilled into afterward; this is just a bookkeeping quirk of the tool, not a sign of an error.
