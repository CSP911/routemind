1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O2, value W2, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01, likely has the answer by origin/value/goods" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of supplier due diligence with different date ranges - need to confirm which applies today (2026-09-21)"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c3da89 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body

2. Answer:
No site visit is required. The file is re-reviewed every 24 months. (For reference, this row also requires a screening score of 53 and last year's financial statements.)

3. Source:
/v1/nodes/hard-diligence-legend-revision/body (confirmed 2026-01-01-onward table is current for today's date, 2026-09-21)
/v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k4/body (the row itself — Site visit: no; Re-review interval: every 24 months)

4. Notes:
Supplier due diligence has three superseded versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), each at a different address and indexed by a different number of qualifiers — the revision-legend page makes clear that reaching for the newest without checking is explicitly the wrong instinct for older dates. For today's date (2026-09-21) the current three-qualifier table (`sec-hard-diligence`) is correct, but the checking step was necessary rather than assumable. The requested row (origin O2, value W2, goods K4) was named exactly by the procurement table's overlay listing, so no guessing or address construction was needed. One oddity: the row's "If the figures are exceeded" footer talks about excess amounts, unrecoverable differences and budget-holder approval — language that reads like it was copied from an expense/threshold table and doesn't obviously apply to a due-diligence row (site visit / re-review cadence). It didn't affect this answer since the two fields asked about are stated plainly in the table above that footer, but it's worth flagging as inconsistent boilerplate in the corpus.
