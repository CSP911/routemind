1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Da Nang supplier, KRW 700,000,000, licence: site visit required? review frequency for file?" --member /v1/regions/procurement "vendor due diligence, site visits, and periodic file review likely live under procurement"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_88e689 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(Da Nang → origin O4, KRW 700,000,000 → value W4 (exact match, "seven hundred million won"), a licence → goods K4. Row O4/W4/K4 also requires a screening score of 93 and audited financial statements for the last three years.)

3. **Source**
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k4/body

4. **Notes**
The procurement table's opening overlay listed three near-identical due-diligence documents flagged "SUPERSEDED" or with version warnings (hard-diligence-legend-revision, hard-diligence-v2, plus the current sec-hard-diligence) alongside an older, unversioned `supplier-due-diligence` overview page. It would have been easy to grab `hard-diligence-v2` by mistake since it sorts near the current table and its description reads plausibly — its own text says it only covers 2024-07-01 to 2025-12-31, so with today's date of 2026-09-20 the current table is `sec-hard-diligence` (in force from 2026-01-01), which is what I used. I did not open `supplier-due-diligence` or `hard-diligence-v2` at all once I saw the "CURRENT" marker on `sec-hard-diligence` and confirmed the row's own footer named 2026-01-01 as its start date.

Mapping the three inputs to codes was mechanical but each legend explicitly warns "this table is the only place the mapping is written down" and to record the choice — 700 million won landed on an exact match (W4) rather than needing a nearest-band judgment call, so no ambiguity there. "A licence" maps to goods K4 by exact wording in the legend, and Da Nang maps to O4 by exact wording — neither required the "take the nearest entry above it" fallback.

The overlay close command reported the four addresses I used as "reached" rather than "used" — I had not formally added them as overlay members before reading them, only the parent procurement table. The outcome was still recorded correctly as answered with all four addresses attached.
