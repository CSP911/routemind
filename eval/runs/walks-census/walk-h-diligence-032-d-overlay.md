1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O1, value W4, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence, need to confirm current version applies to today's date 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_8bffd3 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body

2. **Answer**: Yes, a site visit is required. The file (re-review) interval is every 6 months. (For context: screening score required is 44, and audited financial statements for the last three years are also required.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is current for today's date, 2026-09-21)
- /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k3/body (the row with the site visit and re-review figures)

4. **Notes**: The procurement table flags up front that supplier due diligence has three superseded/current versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and warns that the oldest version doesn't say it was replaced — reaching for the newest table without checking the date would be wrong for a 2025-dated question. Today's date (2026-09-21) falls in the current range, so `sec-hard-diligence` (three-qualifier index) was the right table, and the row for O1/W4/K3 existed directly under it — no interpolation or nearest-match guessing needed. One oddity: closing the overlay reported the row address as "reached" rather than a named member, since I added the parent table (`sec-hard-diligence`) as the overlay member rather than the individual row — worth noting in case that distinction matters for scoring, though it didn't affect finding the answer.
