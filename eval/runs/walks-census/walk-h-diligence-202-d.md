1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body

2. **Answer**
Site visit: no.
Re-review interval: every 36 months.
(Also on the row, though not asked: screening score required 64, financial statements not required.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (used to confirm which version applies)
/v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body (source of the answer)

4. **Notes**
Supplier due diligence has three versions covering different date ranges, and the legend-revision
page warns explicitly that the newest table is wrong for anything before 2026-01-01, and that the
oldest version says nothing about being superseded — so grabbing the first row that looks like a
match without checking dates would be an easy mistake here. Today's date (2026-09-20) falls in the
current version's range (2026-01-01 onward, `sec-hard-diligence`), so no correction was needed, but
the check was worth doing explicitly rather than assuming "current" is always right.

The row itself also carries a trailing "If the figures are exceeded" section about unapproved
excesses and budget-holder approval — boilerplate that reads like it belongs to an expense/threshold
table, not a due-diligence checklist (site visit / re-review interval aren't "figures" you exceed).
It's not relevant to this question and I ignored it, but it's the kind of thing that could mislead
someone into thinking there's a way to skip the site visit or shorten the re-review interval with
approval — the table gives no such mechanism for these two fields.
