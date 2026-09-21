1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O2, value W4, goods K2: site visit required and file review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, likely holds the origin/value/goods matrix" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence rules - need to confirm which version applies today (2026-09-21)"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_cd5c25 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months. (For reference, the screening score required is 59 and audited financial statements for the last three years are needed.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is in force for today's date, 2026-09-21)
- /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k2/body (the actual figures: site visit yes, re-review every 6 months)

4. **Notes**: The overlay create step listed the whole `sec-hard-diligence` table as one member by parent address, but the tool expanded it into all 64 individual origin/value/goods row addresses (4×4×4) plus the legend page — so the "member" I picked wasn't itself a leaf row, it just pulled in the whole matrix. That's fine here since the target row (o2/w4/k2) was directly named among the rows, but it's a place a search could balloon in size without narrowing further. The real risk in this walk was date-based: there's a legend-revision page warning that supplier due diligence has been rewritten three times (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), each indexed differently (one/two/three qualifiers), and it explicitly calls out that grabbing the newest table is wrong for anything dated before 2026-01-01. Today (2026-09-21) does fall under the current three-qualifier table (`sec-hard-diligence`), so no correction was needed, but skipping that check and just reading the first origin/value/goods row that matched would have been an unverified assumption rather than a confirmed one.
