## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body

## Answer
Site visit: no.
Re-review interval: every 24 months.

## Source
/v1/nodes/hard-diligence-legend-revision/body (confirmed 2026-09-20 falls under the current, 2026-01-01-onwards version)
/v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k1/body (the answer)

## Notes
The procurement area flags up front that supplier due diligence has three superseded versions
(`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and warns that reaching for
the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) is safely inside the
current table's range, but I checked the legend-revision page anyway rather than assuming — the
warning explicitly calls out that the oldest version doesn't announce its own replacement, which
is the trap.

The question already gave origin/value/goods as codes (O2, W2, K1) rather than plain-language
descriptions, so there was no need to open the origin/value/goods legend pages to translate a
supplier's real-world attributes into codes — the row address could be built directly from the
codes given.

One oddity worth flagging: the row document ends with an "If the figures are exceeded" section
about unapproved excess amounts and budget-holder sign-off, which reads like boilerplate copied
from an expense/threshold-style page and has nothing to do with site visits or re-review cadence.
It's not part of the answer and could mislead someone skimming for extra conditions on the site
visit or review interval.
