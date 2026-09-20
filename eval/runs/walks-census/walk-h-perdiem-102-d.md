1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s3/body

2. **Answer**
For grade G2, band B1, stay S3 (in force from 2026-01-01): the hotel lodging cap is 167 USD per night. A receipt must be kept for any spend above 28 USD (the receipt threshold).

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s3/body

4. **Notes**
The /v1/regions/expense table flagged up front that overseas per-diem has three versions in force at different times, with the older ones "superseded" but still present in the listing (`hard-perdiem-v2` for 2024-07-01–2025-12-31, and an older `overseas-rates`). It would have been easy to grab one of those by mistake since they sit right next to the current one in the table listing. The row I read confirmed its own validity window ("In force from 2026-01-01") inline, which matches today's date (2026-09-20), so I'm confident this is the current, correct row rather than a superseded one. The exact grade/band/stay combination (G2/B1/S3) had a direct row in the 64-row table, so no interpolation or legend lookup was needed to resolve the codes — the question already gave codes rather than plain-language descriptions.
