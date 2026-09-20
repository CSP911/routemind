## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body

## Answer
No, a site visit is not required. The file is re-reviewed every 36 months.
(For reference, the same row also requires a screening score of 80 and no financial statements.)

## Source
/v1/nodes/hard-diligence-legend-revision/body (confirmed today's date, 2026-09-20, falls under the current table)
/v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body (the answer)

## Notes
The procurement area warns up front that supplier due diligence has THREE versions in force over different date ranges (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and that the oldest version says nothing about being superseded — so grabbing the first "due diligence" table found would silently give a stale answer. I checked the legend-revision page before reading any row, which confirmed 2026-09-20 falls in the current table (`sec-hard-diligence`), so no version confusion here. The row itself was a direct hit — origin/value/goods codes were given in the question, so no need to consult the origin/value/goods legend files separately. One oddity: the row's "If the figures are exceeded" section talks about excess settlement and budget-holder approval, which reads like boilerplate carried over from an expense/threshold-style template rather than content specific to site visits or re-review — it doesn't affect the site-visit/re-review answer but is worth flagging as possibly mismatched content.
