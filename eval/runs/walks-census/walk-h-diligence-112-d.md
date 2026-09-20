1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months. (For reference, this row also requires a screening score of 52 and last year's financial statements.)

3. **Source**
/v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body
(also consulted: /v1/nodes/hard-diligence-legend-revision/body, to confirm which of the three due-diligence table versions applies to today's date)

4. **Notes**
- Procurement has three superseded/current versions of the supplier due diligence table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly against grabbing the newest one by reflex. With today dated 2026-09-20, the current table (`sec-hard-diligence`, in force from 2026-01-01) is correct, but this was the one place a careless walk could have landed on the wrong version.
- The question's O2/W2/K3 codes matched the row-indexing scheme exactly, so no trip to the origin/value/goods legend files was needed to translate plain-language qualifiers into codes — worth flagging in case that's not always true of similarly phrased questions.
- The row document ends with an "If the figures are exceeded" section about unapproved/unavoidable excess and reimbursement — this reads like boilerplate carried over from an expense-type template and has nothing to do with site visits or re-review cadence. It's a plausible spot to get distracted or misquote from; it was ignored for this answer.
