1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months.
(Full row, for context: screening score required 67; financial statements from the last year.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirms which of the three due-diligence versions is current for today's date, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body (the answer)

4. **Notes**
The procurement table flags up front that supplier due diligence has THREE versions in force over different date ranges (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and warns that reaching for the newest is wrong for dates before 2026-01-01. That's the one place this walk could easily go wrong — it would be easy to skip straight to `sec-hard-diligence` since it's labeled "current" and get the right answer by luck, but I checked the legend-revision page explicitly to confirm 2026-09-20 falls in the current version's range before trusting the row. For an older date, `hard-diligence-v2` or `supplier-due-diligence` would be the correct table instead.

Also, the row document itself ends with an "If the figures are exceeded" section that reads like boilerplate carried over from an expense-report template (excess claims, budget holder sign-off) — it doesn't relate to site visits or re-review intervals and looks like a mismatched fragment. I ignored it since it doesn't bear on this question, but it's worth flagging as a possible authoring error in the source.
