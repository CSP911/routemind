1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O1, value W1, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "premises visit and file review cadence sound like vendor/supplier due diligence, which procurement covers"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_96ebe3 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body

2. **Answer**: No, a site visit is not required. The file is re-reviewed every 36 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions applies to today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body (the row with the figures: Site visit = no, Re-review interval = every 36 months)

4. **Notes**: The supplier due diligence subject has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend page warns that the oldest version says nothing about being superseded — so grabbing the first plausible-looking row without checking the revision legend would have risked answering from a table that's two versions stale. Today's date (2026-09-20) falls under the current table, `sec-hard-diligence`, so that risk didn't materialize here, but it was worth checking explicitly rather than assuming "current" was safe by default. The row itself was found directly at the expected address (`hard-diligence-row-origin-o1-value-w1-goods-k2`) once the three qualifiers were known, no ambiguity there. One oddity: the row document ends with an "If the figures are exceeded" section about excess costs and budget-holder approval, which reads like boilerplate carried over from an expense-report template rather than content relevant to a due-diligence checklist — it wasn't used in the answer since it doesn't pertain to site visits or review cadence.
