1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W4, goods K1: site visit required? review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, likely holds the O3/W4/K1 row" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions, need to confirm which is in force for today's date 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0d3f18 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Also on this row, for context: screening score required is 74; financial statements needed are the last three years, audited.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which version is in force for today's date, 2026-09-20/21 → the current table)
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k1/body (the answer itself)

4. **Notes**
Opening the procurement region table already listed the exact row address (`hard-diligence-row-origin-o3-value-w4-goods-k1`) among its 68 rows, since the region-level table shows the full origin×value×goods matrix rather than just the top-level nodes — so no legend lookups for O3/W4/K1 codes were actually needed to find the row. The one thing worth checking carefully was the version: procurement's table explicitly warns supplier due diligence has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls cleanly in the current (2026-01-01 onward) version, so `sec-hard-diligence` / the row I read was correct, but this is exactly the kind of question where grabbing the first matching row without checking the effective-date legend would have risked citing the wrong version if the question had been dated differently. The overlay close reported the row as "reached" rather than a named member since I'd only added the parent table `sec-hard-diligence` as a member, not the specific row — harmless, but worth noting for how the tool tracks provenance.
