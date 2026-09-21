1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Da Nang supplier, KRW 8,000,000, office consumables: site visit required? file review frequency?" --member /v1/regions/procurement "supplier due diligence, site visits, and file review cadence are procurement policy topics"
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_510f50 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body

2. **Answer**
No site visit is required. The file gets re-reviewed every 36 months. (Screening score required: 78; financial statements not required.) This is under the current supplier due diligence table, in force from 2026-01-01, which applies as of today (2026-09-21).

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body (office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body (the answer: site visit no, re-review every 36 months)

4. **Notes**
- The overlay's initial member list surfaced 15 rows under /v1/regions/procurement, including three different versions of the supplier due diligence table (current, `hard-diligence-v2` superseded 2024-07-01 to 2025-12-31, and an even older `supplier-due-diligence`, plus a `hard-diligence-legend-revision` warning page). It would be easy to grab a superseded row by accident — I went straight for `sec-hard-diligence`, the one explicitly labeled "THE CURRENT ... in force from 2026-01-01," and confirmed the row itself restates that effective date, which covers today (2026-09-21).
- The table is addressed by three independent codes (origin, value band, goods category) that must each be looked up in a separate legend file before the right row address can be built — none of the codes are guessable from the question's plain-language terms, and getting any one wrong (e.g. picking a neighboring value band) silently gives you a different, wrong row with no error.
- The `overlay close` command flagged all four addresses I used as "reached = answered from somewhere the overlay never named" — I read the legend/row files directly via `read` rather than first adding them to the overlay with `overlay add`. The close still recorded them correctly as used, but the intended workflow was apparently to add each address to the working set before reading it.
