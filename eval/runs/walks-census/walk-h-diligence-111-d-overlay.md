1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O2, value W2, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "vendor/site visit requirement and review frequency by origin/value/goods risk tier sounds like procurement due diligence"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_bf02dc --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body

2. **Answer**: No, a site visit is not required. The file (screening) gets re-reviewed every 24 months. (Also on this row: screening score required 51, financial statements from the last year — not asked for, but part of the same row.)

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body
/v1/nodes/sec-hard-diligence
/v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body

4. **Notes**: This table has three superseded versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no version marked withdrawn — the legend-revision page is explicit that the oldest version says nothing about being replaced, so grabbing the first due-diligence table found under procurement without checking dates would silently give a 2024-era answer for a 2026 question. Today's date (2026-09-20/21) falls in the "2026-01-01 onwards" band, so `sec-hard-diligence` is correct here, but this is exactly the kind of row where reaching for "the newest" without checking would have been right by luck rather than by method. The row itself also carries a boilerplate "If the figures are exceeded" section about approved/unapproved excess and budget-holder decisions that reads like it was copy-pasted from an expense/threshold-style document and doesn't actually apply to a due-diligence row (there's no "figure" being exceeded here) — worth flagging as noise, not part of the answer. Separately, `overlay close --used` reported all three addresses as "reached" rather than matched members, because I only ever added the parent `/v1/regions/procurement` table as a member and then read the leaf documents directly rather than running `overlay add` for each one — the close still recorded them, but the working set wasn't kept as rigorously as intended.
