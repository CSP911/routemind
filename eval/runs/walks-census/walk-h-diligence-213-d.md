1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body

2. **Answer**
No site visit required. Re-review interval: every 24 months.
(For reference, this row also requires a screening score of 69 and financial statements from the last year.)

3. **Source**
/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k4/body

4. **Notes**
Checked /v1/nodes/hard-diligence-legend-revision/body first because the procurement table listing warned that supplier due diligence has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward) and that reaching for the newest by default is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls in the current version's window, so `/v1/nodes/sec-hard-diligence` was the correct table to use — but this was worth confirming explicitly rather than assuming, since the older `hard-diligence-v2` and `supplier-due-diligence` pages give no indication in themselves that they've been superseded. The current table listed all 64 origin/value/goods rows directly, including an exact match for O3/W2/K4, so no interpolation or legend lookup (for origin/value/goods code meanings) was needed — the row address was unambiguous.
