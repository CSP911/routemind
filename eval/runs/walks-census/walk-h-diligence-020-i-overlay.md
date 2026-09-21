1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Company in Daejeon, 300M won, office consumables only: is a site visit required, and how often is the file reviewed again?" --member /v1/regions/procurement "vendor due diligence / site visit and review cadence would be under procurement"
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_ee1c6a --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months.

3. **Source**:
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → origin O1)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3)
- /v1/nodes/hard-diligence-legend-goods/body (just office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k1/body (the row: Site visit = yes, Re-review interval = every 12 months)

4. **Notes**: The procurement overlay surfaced two near-duplicate legend/table sets for supplier due diligence — a "legend revision" warning node and superseded version `hard-diligence-v2` (in force 2024-07-01 to 2025-12-31), plus an even older `supplier-due-diligence`. It would have been easy to grab a row from the wrong-dated table. I stuck with `sec-hard-diligence`, which states it is "THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-01-01," and today is 2026-09-20, so that's the correct one — I didn't open the superseded versions since the current table's own header was unambiguous about being in force. The three legend tables (origin, value, goods) each translate the plain-language description into a code (O1/W3/K1) and explicitly warn that the mapping is "the only place" it's written down, so skipping them and guessing the row address would have been the wrong move. The overlay close reported these addresses as "reached" rather than the originally declared members, since I drilled into the row and legend files directly rather than adding them to the overlay first — functionally the same evidence trail, just flagged as such by the tool.
