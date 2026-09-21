1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W1, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods - likely holds premises visit and re-review frequency" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table, need to confirm which is current as of 2026-09-21" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together, may clarify premises visit / review cadence terminology"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_682ba6 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body

2. **Answer**:
No, a site visit is not required. The file (screening) is re-reviewed every 36 months.
(For reference, this row also requires a screening score of 64 and does not require financial statements.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is current for a question dated 2026-09-21 — the current table, in force from 2026-01-01)
- /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k3/body (the row with the site-visit and re-review figures)

4. **Notes**:
The row address for exactly this combination (origin O3, value W1, goods K3) was already printed verbatim in the overlay table under the `sec-hard-diligence` member, so no guessing or address construction was needed — it appeared alongside all 64 other origin/value/goods combinations. The one place this could have gone wrong is the due-diligence table's version history: there are three versions of this table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), each indexed differently, and the legend-revision page explicitly warns that reaching for the newest is wrong for older dates. Today's date (2026-09-21) falls in the current version's range, so `sec-hard-diligence` / the `hard-diligence-row-origin-o3-value-w1-goods-k3` address was correct — but this was worth checking explicitly rather than assuming "current" was right by default. The overlay close reported the row as "reached" rather than a listed member, since it was never separately added as its own overlay member (it came pre-listed under the `sec-hard-diligence` table entry) — the answer is unaffected by this bookkeeping distinction.
