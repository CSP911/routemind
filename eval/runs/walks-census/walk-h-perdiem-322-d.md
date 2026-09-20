1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body

2. **Answer**: For grade G4, band B3, stay S3 (in force from 2026-01-01, current as of today 2026-09-20): lodging cap is 327 USD per night. A receipt must be kept for any spend above 54 USD (the receipt threshold).

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body

4. **Notes**: The expense area's table listing flags that overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), so it would have been easy to grab an old rate table by mistake — I confirmed `sec-hard-perdiem` is explicitly labeled as "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01" and today's date (2026-09-20) falls within that window, so no need to consult the legend-revision file further. The row address itself already encoded the exact grade/band/stay combination requested, so no legend lookups (grade/band/stay code mapping) were needed since the question was given in G4/B3/S3 code form directly rather than in plain-language terms.