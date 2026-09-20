## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body

## Answer
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Full row for reference: screening score required 86, financial statements for the last two years.)

## Source
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is current as of 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body (the answer)

## Notes
The procurement area lists three superseded/live versions of the supplier due diligence subject
(`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), with an explicit warning page
saying the newest is not always right and a 2025-dated question would need the middle version. Today's
date (2026-09-20) falls after the current table's 2026-01-01 start, so `sec-hard-diligence` was correct,
but it would have been easy to skip the legend/warning check and just grab the first "supplier due
diligence" hit in the procurement table listing — that first hit is the outdated one indexed by only
one qualifier, not the three-qualifier current table. Worth being deliberate about checking the revision
legend before reading a row.

The row document's closing "If the figures are exceeded" section talks about excess amounts, budget
holders, and unapproved overages — language that reads like it was copied from an expense/spend-limit
table rather than written for a due-diligence checklist (site visit / screening score / re-review
interval). It doesn't answer anything asked here and doesn't contradict the figures above, but it's an
odd, seemingly mismatched boilerplate block worth flagging rather than silently ignoring.
