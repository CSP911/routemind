## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body

## Answer
Site visit: no.
Re-review interval: every 24 months.
(Screening score required: 84; financial statements: last year — not asked but part of the same row.)

## Source
/v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k3/body

## Notes
- Supplier due diligence has three versions at three different addresses (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the oldest one gives no indication it was ever superseded. The `hard-diligence-legend-revision` page is the only thing that tells you a date check is required before picking a table — worth reading before trusting any diligence row, since guessing "newest" would have been right here (today is 2026-09-20, current table is in force from 2026-01-01) but is explicitly called out as wrong for 2025-dated questions. Easy to get lucky and not realize the check was needed.
- The current table (`sec-hard-diligence`) is indexed directly by origin/value/goods codes, and the question already gave the codes (O4, W2, K3) rather than descriptions — so the origin/value/goods legend pages turned out not to be needed. In a question phrased with plain-language descriptions instead of codes, those legends would be required to pick the right row; worth being alert to that difference.
- The row's closing paragraph ("If the figures are exceeded... decided by the budget holder") reads like boilerplate carried over from an expense/threshold-style table — it doesn't obviously apply to a site-visit/re-review row, which has no "figure" to exceed. I did not use it for the answer and flag it here as a possible templating artifact rather than a fact about diligence rows.
