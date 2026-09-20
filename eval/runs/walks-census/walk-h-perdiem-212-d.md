1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body

2. **Answer**: For grade G3, band B2, stay S3 (current table, in force from 2026-01-01): lodging cap is 247 USD per night. A receipt must be kept for any spend above 41 USD (the receipt threshold).

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s3/body

4. **Notes**: The `/v1/regions/expense` table warns that overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), so it would have been easy to grab a stale rate — I went straight for `sec-hard-perdiem`, which the region table and the row document both confirm is the one in force from 2026-01-01, matching today's date. The row itself lists four figures (lodging, meals, receipt threshold, incidentals); the question only asked about the hotel/night cap and the receipt-keeping threshold, so I pulled just those two rather than the whole table. Didn't need to open the legend files since the question already gave grade/band/stay codes directly.
