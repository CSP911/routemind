1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body

2. **Answer**
No site visit is required. The file (re-review) is looked at again every 36 months. (For completeness, the same row also requires a screening score of 79 and no financial statements.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions is current for today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body (the answer)

4. **Notes**
Supplier due diligence has three superseded versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01 — the oldest version doesn't even say it was replaced. Since today is 2026-09-20, the current table (`sec-hard-diligence`, in force from 2026-01-01) is correct, but this was worth checking rather than assuming. The row for O4/W1/K2 existed directly under the current table's listing, so no legend lookup for origin/value/goods codes was needed. One odd note: the row document's closing section ("If the figures are exceeded") talks about an excess, budget holder, and recoverability — language that reads like it belongs to an expense/spend-limit table, not a due-diligence checklist about site visits and re-review intervals. It doesn't affect the site-visit or re-review answer, but it looks like boilerplate copied from a different table and is worth flagging as a possible inconsistency in the source data.
