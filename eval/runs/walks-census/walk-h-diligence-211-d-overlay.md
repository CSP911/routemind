1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W2, goods K2: is a premises visit required, and how often is the file reviewed again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods" --member /v1/nodes/hard-diligence-legend-revision/body "warning about three versions of due diligence, need to confirm which is current for 2026-09-21" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a60137 --outcome answered --used /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**
No premises (site) visit is required. The file is re-reviewed every 24 months.
(Also on the row, for context: screening score required 67, financial statements from last year — not asked for but part of the same row.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions applies to a 2026-09-21 question — the current one)
/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body (the actual figures: site visit no, re-review every 24 months)

4. **Notes**
- The procurement area table names three versions of supplier due diligence with no indication in the top-level listing of which is "current" for a given date — the legend-revision page is what actually settles that, and it explicitly warns that reaching for the newest version is wrong for anything dated before 2026-01-01. Since today is 2026-09-21, the current table (`sec-hard-diligence`, in force from 2026-01-01) is correct, but this was a step I made a point of checking rather than assuming.
- The current table is indexed by all three qualifiers (origin, value, goods) as separate rows, one per combination — O3/W2/K2 pointed straight at a single row address, no ambiguity there.
- The row's body ends with an "If the figures are exceeded" section about unapproved excesses and budget-holder sign-off — that reads like boilerplate carried over from an expense/threshold-style template rather than something meaningful for a due-diligence checklist (site visit / re-review interval aren't "figures" that get "exceeded" the way an amount would). I did not use it in the answer since it doesn't actually apply to the site-visit/re-review question, but it's the one place in this row that felt out of place and worth flagging.
