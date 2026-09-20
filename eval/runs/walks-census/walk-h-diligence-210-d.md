1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months. (For context, this row also requires a screening score of 66 and last year's financial statements.)

3. **Source**
/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k1/body

4. **Notes**
The procurement area lists three versions of the supplier due diligence table (old, `hard-diligence-v2`, and current `sec-hard-diligence`), with an explicit warning page (`hard-diligence-legend-revision`) saying the newest table is wrong for anything dated before 2026-01-01. Today's date (2026-09-20) falls under the current table, so no version confusion here, but this is exactly the kind of question where grabbing the first "supplier due diligence" hit would have risked landing on the superseded v2 table instead of `sec-hard-diligence` — worth checking the legend page on every diligence question, not just ones that look old. The question's O3/W2/K1 codes matched the row-address naming convention directly, so no need to open the origin/value/goods legend files to translate plain-language qualifiers into codes.
