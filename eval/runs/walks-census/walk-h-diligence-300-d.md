## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body

## Answer
No — site visit is not required. Re-review interval: every 36 months.
(For context, screening score required is 78 and financial statements are not required for this row.)

## Source
- /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k1/body (site visit / re-review figures)
- /v1/nodes/hard-diligence-legend-revision/body (confirms this row's table, in force 2026-01-01 onward, is the correct version for today's date 2026-09-20)

## Notes
The origin/value/goods code (O4, W1, K1) went straight to a row address on the current diligence table (`sec-hard-diligence`) without needing the legend pages for origin/value/goods — the question already gave codes rather than plain-language descriptions, so no code lookup was needed there.

The near-miss was version, not row: procurement lists three eras of "supplier due diligence" (`supplier-due-diligence`, `hard-diligence-v2`, and the current `sec-hard-diligence`), all still present and none marked withdrawn. The table listing under `/v1/regions/procurement` flags this explicitly ("supplier due diligence has THREE versions"). It would have been easy to grab the first plausible-looking diligence row without checking which era it belonged to. I confirmed via `hard-diligence-legend-revision` that 2026-01-01 onward is current and today (2026-09-20) falls in that range, and the row itself also self-declares "In force from 2026-01-01," so the two sources agree.
