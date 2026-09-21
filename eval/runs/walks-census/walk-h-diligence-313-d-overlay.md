1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O4, value W2, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin/value/goods, in force since 2026-01-01" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table, need to confirm which is current for today's date"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e33980 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months. (Screening score required: 85; financial statements: last year — not asked for but on the same row.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body
/v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body

4. **Notes**
Supplier due diligence has three versions at different addresses (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page is explicit that reaching for the newest is wrong for anything dated before 2026-01-01 — the older table doesn't even say it was superseded, so nothing on its own page would warn you off it. Today's date (2026-09-20/21) falls after 2026-01-01, so the current three-qualifier table (`sec-hard-diligence`) was correct, but this is exactly the trap the page calls out: skipping that check and just grabbing the newest-looking table would have happened to be right here, for the wrong reason. Worth flagging for future walks with earlier dates.

Minor: creating the overlay with the two table-level members auto-expanded into the full 4×4×4 row grid (64 rows) rather than staying at two rows — the specific O4/W2/K4 row I ended up reading wasn't one of the two addresses I named as members, so the close command reported it as "reached" rather than a named member. Not an error, just worth noting the overlay listing is coarser than the members you actually specify.
