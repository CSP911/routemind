1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body

2. Answer
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Also on this row, for context: screening score required 40; financial statements for the last two years.)

3. Source
/v1/nodes/hard-diligence-row-origin-o1-value-w3-goods-k3/body
(reached via /v1/nodes/sec-hard-diligence, confirmed as the current version via /v1/nodes/hard-diligence-legend-revision/body)

4. Notes
Supplier due diligence has three superseded versions (`supplier-due-diligence`, then `hard-diligence-v2` for 2024-07-01–2025-12-31, then `sec-hard-diligence` for 2026-01-01 onwards), and the legend page warns the oldest version doesn't say it was replaced. Today is 2026-09-20, so the current table applies — but this is exactly the kind of question where grabbing the first "supplier due diligence" hit without checking dates would silently give an outdated answer. Worth flagging: the row's own "If the figures are exceeded" section talks about excess amounts and budget-holder approval — boilerplate that reads like it belongs to an expense/threshold table, not a due-diligence checklist. I ignored it since it doesn't bear on the site-visit or re-review question, but it's an odd inconsistency in the document.
