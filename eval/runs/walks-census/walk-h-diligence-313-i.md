1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body

2. **Answer**
No site visit is required. The file is re-reviewed every 24 months.
(For this row: screening score required 85, financial statements from last year.)

3. **Source**
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → value W2)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
- /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k4/body (the answer: site visit no, re-review every 24 months)

4. **Notes**
The procurement area lists three versions of the supplier due diligence rules (a legend-revision warning page, a superseded `hard-diligence-v2`, and an older `supplier-due-diligence`). It would be easy to grab the wrong version's row by mistake. I used `sec-hard-diligence`, which is explicitly labeled "THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-01-01" — today is 2026-09-20, so this is the correct, currently-effective table, and I didn't need to consult the legend-revision or superseded pages at all.

The three legends (origin, value, goods) are each separate documents and none of them repeat the mapping shown by the others, so all three had to be fetched individually before the row address could be assembled — nothing in the table listing told me the code combination directly. "A licence" as a goods category was the least obvious of the three to match; it happened to be an exact wording match in the legend table, so no interpretation was needed, but if it hadn't been I'd have had to fall back to "nearest entry above it" per the legend's own instruction.
