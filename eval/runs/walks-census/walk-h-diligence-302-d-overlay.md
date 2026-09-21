1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W1, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "diligence/site-visit and review-frequency rules by origin, value, goods category sound like procurement due-diligence thresholds"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e085dd --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body

2. **Answer**: No site visit is required. The file (screening) is re-reviewed every 36 months. (For reference, the screening score required is 80 and financial statements are not required for this row.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is in force for today's date, 2026-09-20/21)
- /v1/nodes/hard-diligence-row-origin-o4-value-w1-goods-k3/body (the row itself, origin O4 / value W1 / goods K3)

4. **Notes**: The overlay's own working set surfaced two older due-diligence tables (`supplier-due-diligence` and `hard-diligence-v2`) alongside the current one (`sec-hard-diligence`), each indexed by a different number of qualifiers (one, two, three respectively) — reaching for the newest-looking table without checking the legend-revision page would have been fine here since today's date (2026-09-20) falls after 2026-01-01, but the revision page's own warning ("the oldest says nothing at all about having been replaced") makes clear this is a trap for questions dated in 2025 or earlier, so I checked it explicitly before trusting `sec-hard-diligence`. No other ambiguity: the three qualifiers (O4, W1, K3) mapped directly onto one row with no interpretation needed. The row's boilerplate "If the figures are exceeded" section talks about excess/budget-holder approval, which reads like it was copy-pasted from an expense-limits template and doesn't actually apply to site-visit/re-review fields — I did not use it in the answer, but flagging it as an oddity in the source document.
