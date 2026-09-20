1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months.
(For reference, this row also requires a screening score of 35 and last year's financial statements.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions applies to today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body (the answer)

4. **Notes**
- There are three versions of the supplier due diligence table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page warns the oldest version "says nothing at all about having been replaced" — it would be easy to land on it by mistake if you just searched for "supplier due diligence" without checking dates. Checked the legend first and confirmed 2026-09-20 falls under the current table (`sec-hard-diligence`), so no ambiguity in the end, but this is the step where a wrong answer would most easily happen.
- The table at /v1/nodes/sec-hard-diligence lists all 64 origin/value/goods combinations directly by address, so the O1/W2/K2 row could be read straight off the listing without needing a separate lookup table for the three qualifiers (origin, value, goods) — I didn't need the individual legend pages since the row address itself was unambiguous.
- The row document ends with an "If the figures are exceeded" section talking about unapproved excess and budget-holder sign-off — this reads like boilerplate carried over from an expense-report template and has nothing to do with site visits or re-review intervals. It's a red herring; ignored it for the answer but flagging it as confusing filler that doesn't belong on a due-diligence page.
