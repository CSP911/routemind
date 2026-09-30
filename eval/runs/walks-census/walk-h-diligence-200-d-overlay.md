1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W1, goods K1, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin, value, goods - primary candidate" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table, need to confirm which is in force today"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5c2f94 --outcome answered --used /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**
No site visit is required. The file is re-reviewed every 36 months.
(Screening score required: 62; financial statements not required — for context, not asked.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body — confirms today's date (2026-09-20/21) falls under the "2026-01-01 onwards, current" version, i.e. the three-qualifier table `sec-hard-diligence`, not the superseded v2 or the original.
/v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body — the actual figures used for the answer.

4. **Notes**
Creating the overlay with `sec-hard-diligence` as a member auto-expanded it into all 64 origin/value/goods row addresses (O1–O4 × W1–W4 × K1–K4), so the exact row for O3/W1/K1 was visible immediately without a separate table fetch — convenient, but it meant the row address was never explicitly added as an overlay member. When closing with `--used` naming that row, rmcli flagged it as "reached" rather than "member" ("answered from somewhere the overlay never named") — harmless here since it's still a real address from the working set's own table, but worth noting as a rough edge in how the overlay tracks provenance.

The real trap in this domain is the three-version history of the due diligence table (`supplier-due-diligence` until 2024-07-01, `hard-diligence-v2` 2024-07-01–2025-12-31, `sec-hard-diligence` current from 2026-01-01). The row addresses under the current table are three-qualifier (origin-value-goods), matching this question's format, which was a useful sanity check that I had the right version — but I still read the legend-revision page explicitly to confirm rather than assume, since the table's own description already claiming "current" is exactly the kind of claim that page warns not to take on faith.
