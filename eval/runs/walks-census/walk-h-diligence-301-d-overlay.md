1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W1, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "diligence/site-visit/review-cycle questions look like supplier risk criteria, likely under procurement"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_1a66f4 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body

2. **Answer**
Site visit: no (not required).
Re-review interval: every 36 months.
(Screening score required: 79; financial statements not required — for context.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of three versions of the due-diligence table is in force for today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k2/body (the answer)

4. **Notes**
Supplier due diligence exists as three separate, non-superseding versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the oldest one says nothing about being replaced — a naive search could easily land on the wrong version if it weren't for the legend-revision warning page. Today's date (2026-09-20) falls after 2026-01-01, so `sec-hard-diligence` (the three-qualifier-indexed current table) is correct; a question dated in 2025 would need `hard-diligence-v2` instead. Worth flagging: the row document's closing section ("If the figures are exceeded") reads like boilerplate about expense/travel overages and doesn't obviously belong to a due-diligence row — it looks like reused template text rather than content relevant to site visits or review cycles, so I ignored it for the answer. The overlay's `close` step reported both addresses as "reached" rather than "used from the working set," since I opened the row directly from the `sec-hard-diligence` table rather than adding it to the overlay first — functionally fine, just a workflow wrinkle.
