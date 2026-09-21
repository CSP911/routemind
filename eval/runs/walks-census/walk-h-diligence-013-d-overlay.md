1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O1, value W2, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "site visit and file review frequency for supplier/vendor due diligence sounds procurement-related"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c49740 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body

2. **Answer**: No, a site visit is not required. The file is re-reviewed every 24 months. (Screening score required: 37; financial statements: last year — noted for context though not asked.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions is in force for today's date, 2026-09-20/21)
- /v1/nodes/sec-hard-diligence (current table, in force 2026-01-01 onwards; located the exact O1/W2/K4 row address)
- /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k4/body (the row itself, giving "Site visit: no" and "Re-review interval: every 24 months")

4. **Notes**: The procurement table carries a loud warning that supplier due diligence has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onwards) and that reaching for the newest by reflex is wrong for anything dated before 2026-01-01 — the legend explicitly calls out 2025 as the trap case. Today's date (2026-09-20/21) falls cleanly in the current-table window, so `sec-hard-diligence` was the right pick, but I read the legend first rather than assuming, since the warning made clear that assuming is exactly the failure mode this page exists to catch. No other ambiguity: the three qualifiers (O1, W2, K4) matched a single row with no aliasing or synonym issues.
