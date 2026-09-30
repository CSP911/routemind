1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Da Nang supplier, 8M KRW, licence: site visit required? review frequency for their file?" --member /v1/regions/procurement "procurement area covers vendor approval/diligence thresholds"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body
./bench/rmcli.py overlay add --id ov_2026-09-20_b34e14 --address /v1/nodes/hard-diligence-legend-origin/body --why "maps Da Nang to origin O4"
./bench/rmcli.py overlay add --id ov_2026-09-20_b34e14 --address /v1/nodes/hard-diligence-legend-value/body --why "maps 8M won to value W1"
./bench/rmcli.py overlay add --id ov_2026-09-20_b34e14 --address /v1/nodes/hard-diligence-legend-goods/body --why "maps licence to goods K4"
./bench/rmcli.py overlay add --id ov_2026-09-20_b34e14 --address /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body --why "answer row: site visit no, re-review every 36 months"
./bench/rmcli.py overlay close --id ov_2026-09-20_b34e14 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body

2. **Answer**:
No site visit is required. The file is re-reviewed every 36 months.
(Also on the row, for context: screening score required is 81; financial statements not required.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (established which of three due-diligence versions applies to a 2026 question)
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
- /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k4/body (the answer row: site visit no, re-review every 36 months)

4. **Notes**:
The supplier due diligence subject has three versions in force over different date ranges, and the legend-revision page is explicit that reaching for the newest is wrong for anything before 2026-01-01 — the oldest version doesn't even say it was superseded, so nothing in that page itself would warn you off it. Today's date (2026-09-20/21) put this squarely in the current table (`sec-hard-diligence`, in force from 2026-01-01), so I didn't have to reason through the superseded versions, but I would have picked the wrong document without checking that page first. The three qualifiers (origin, value, goods) each had their own legend page rather than being spelled out in the row table itself, so all three had to be read before the row address could even be constructed — a step easy to skip if you assume the row list's descriptions ("origin O4, value W1, goods K4") are self-explanatory without checking what those codes mean for this specific supplier. No ambiguity in the mapping itself: Da Nang, 8M won, and "a licence" each matched a legend entry exactly.
