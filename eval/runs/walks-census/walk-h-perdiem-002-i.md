1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body

2. **Answer**
A junior analyst on an 8-night trip to Tokyo (grade G1, band B1, stay S3) can put up to 103 USD per night on the hotel. A receipt must be kept for any spend above 24 USD (the receipt threshold on the same row). This is under the per-diem table in force since 2026-01-01, which applies to today's date (2026-09-20).

3. **Source**
- /v1/regions/expense (found the current per-diem table and the warning that three versions exist)
- /v1/nodes/sec-hard-perdiem (index of the current, 2026-01-01-forward table)
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → G1)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → B1)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → S3)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s3/body (lodging cap 103 USD/night, receipt threshold 24 USD)

4. **Notes**
- The expense region table flags up front that overseas per-diem has three versions in force at different times (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`). It would be easy to grab the wrong one — I picked `sec-hard-perdiem` because it's explicitly labeled current since 2026-01-01, and today (2026-09-20) falls inside that range. I didn't open the legend-revision doc since the row itself restated the effective date and confirmed the superseded chain, but a stricter walk might open it anyway to double check nothing more recent had superseded this table.
- "Eight nights" maps exactly onto the S3 legend entry ("eight nights") — no rounding or nearest-match judgment call was needed here, unlike grade/band which are more literal lookups.
- The receipt threshold turned out to live on the same per-diem row as the lodging cap, not in the separate `/v1/nodes/evidence` table one level up — I almost went to open that table for the receipt-threshold half of the question before noticing the row already answered it.
