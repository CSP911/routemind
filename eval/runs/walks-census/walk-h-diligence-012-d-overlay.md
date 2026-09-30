1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O1, value W2, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods - likely has the site visit and file review columns" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table with different date ranges - need to confirm which is in force today 2026-09-20" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together, may clarify terms like premises visit / file review"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_df7240 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k3/body

2. **Answer**
No site visit required. File (re-review) interval: every 24 months.

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed the current, three-qualifier table applies for a 2026-09-20 question)
/v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k3/body (the actual figures)

4. **Notes**
The "current" table (`sec-hard-diligence`) is indexed by three qualifiers (origin, value, goods) and is in force from 2026-01-01 — the legend-revision page makes clear this is a live subject with three overlapping-looking versions (one-qualifier, two-qualifier, three-qualifier), and that reaching for the newest is only correct because today's date (2026-09-20) falls after 2026-01-01. Worth checking every time since the middle version would answer a 2025-dated question instead.

The row's boilerplate "If the figures are exceeded" section (about unapproved/unavoidable excess, budget-holder sign-off) reads like it was copied from an expense-report template and has nothing to do with site visits or re-review timing — ignored it, but it could mislead someone skimming for "what happens if we skip the visit."

Minor mechanical note: the overlay's `close` command reported the row address I actually used as "reached" rather than a named member, since I read it directly (it was only visible as a row printed under the `sec-hard-diligence` member, not added individually via `overlay add`). Didn't affect the answer, but the overlay's bookkeeping only credits addresses explicitly added as members.
