1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 6 months.
(For reference, this row also requires a screening score of 77 and audited financial statements for the last three years.)

3. **Source**
/v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k4/body
(supporting: /v1/nodes/hard-diligence-legend-revision/body, used to confirm the current 2026-01-01-onward table applies to today's date 2026-09-20)

4. **Notes**
The procurement area's table lists three due-diligence documents (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no obvious warning at that level about which is current. The `hard-diligence-legend-revision` page makes clear this is a trap: the oldest version doesn't say it was superseded, and for a 2025-dated question the correct answer would have been the middle version, not the current one. Since today is 2026-09-20, `sec-hard-diligence` (in force 2026-01-01 onward) was the right table to use — worth flagging that this same walk on a different "today" would land on a different document entirely.

The question already gave origin/value/goods as codes (O3, W4, K4) rather than plain-language descriptions, so no legend lookup (goods/origin/value legends) was needed to resolve which row applied — the row address matched directly. Had the question used descriptive language instead of codes, those three legend pages would have been required first.
