1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body

2. **Answer**
No site visit required. Re-review interval: every 36 months.
(For reference, screening score required is 48 and financial statements are not required for this row.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three diligence versions applies to today's date)
/v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k3/body (the answer)

4. **Notes**
Supplier due diligence exists in three superseded/current versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend page explicitly warns that the oldest version never says it was replaced — reaching for whichever page looked newest without checking the revision legend would have been an easy way to grab a stale row. Today (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` is correct; had the question been dated in 2025 the answer would have come from `hard-diligence-v2` instead, and pre-2024-07-01 from the original `supplier-due-diligence` page. The current table is indexed by exactly the three qualifiers given (origin, value, goods), so the row address could be built directly from the pattern once the legend confirmed the active version — no ambiguity there. One oddity: the row's "If the figures are exceeded" section talks about excesses and budget-holder approval, which reads like boilerplate carried over from an expense/threshold-style template and doesn't obviously apply to site-visit/re-review policy — it wasn't needed to answer this question but is worth flagging as a possible template mismatch in the source content.
