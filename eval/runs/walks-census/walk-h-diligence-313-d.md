1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body

2. Answer
No site visit is required. The file is re-reviewed every 24 months.
(Also on this row, though not asked: screening score required 85, financial statements from last year.)

3. Source
/v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body

4. Notes
Supplier due diligence has three versions in force over different date ranges (until 2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onwards), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls in the current version's range, so `sec-hard-diligence` was correct, but this was the one place the walk could easily have gone wrong — a naive approach might grab the first "supplier due diligence" table found without checking which of the three versions applies to the current date. I deliberately checked the legend-revision page before opening the row.

The row's closing section, "If the figures are exceeded," talks about an unapproved/unavoidable excess being settled or claimed with a budget holder — this reads like boilerplate carried over from an expense/threshold-style template and doesn't actually apply to the due-diligence fields (screening score, site visit, re-review interval) on this page. It's a bit disorienting but not relevant to the question asked, so I did not fold it into the answer.
