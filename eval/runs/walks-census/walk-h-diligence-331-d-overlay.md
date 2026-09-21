1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O4, value W4, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "diligence/premises visit and review frequency by category/amount/origin sounds like procurement approval matrix"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_db3c96 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 6 months. (For reference, the screening score required is 91 and audited financial statements for the last three years are also required.)

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body
/v1/nodes/hard-diligence-row-origin-o4-value-w4-goods-k2/body

4. **Notes**: The supplier due diligence subject has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onwards), and the legend-revision page warns that the oldest version never says it was superseded, so grabbing the first hit without checking the date would silently give stale figures. Today's date (2026-09-20) falls in the current version's range, so `sec-hard-diligence` was correct, but this is exactly the kind of question where reaching for "the newest table" without checking would happen to be right for the wrong reason — the check still had to be made. Once in the current table, the origin/value/goods row address was printed directly and matched exactly, no ambiguity there.
