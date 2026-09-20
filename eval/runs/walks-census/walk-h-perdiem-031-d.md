1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body

2. **Answer**: For grade G1, band B4, stay S2: lodging cap is 147 USD per night, and the receipt threshold is 48 USD — spends above that amount require a receipt to be kept. (For context, meals are 85 USD/day and incidentals 17 USD/day.) In force since 2026-01-01, which covers today's date (2026-09-20).

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body

4. **Notes**: The expense region's table listing flagged that overseas per-diem has three versions in force at different times (a legend node, `hard-perdiem-legend-revision`, and superseded tables `hard-perdiem-v2` and `overseas-rates` both still sit in the region listing). It would be easy to grab a superseded rate table by mistake. I went straight to `/v1/nodes/sec-hard-perdiem`, which is explicitly labeled "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01," and confirmed the row itself restates that it's in force from 2026-01-01 and names the superseded predecessors — so today's date (2026-09-20) falls within its validity and no version confusion applies here. The row address matched the exact grade/band/stay combination directly from the table listing, so no legend lookups (grade/band/stay definitions) were needed since the question already gave codes G1/B4/S2 rather than plain-language descriptions.
