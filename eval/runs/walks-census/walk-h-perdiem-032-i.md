1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s3/body

2. **Answer**: A junior analyst on an 8-night Dhaka trip is grade G1, band B4, stay S3. The nightly lodging cap is 151 USD. A receipt is required for any spend above 51 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s3/body

4. **Notes**: The expense region table flags that overseas per-diem has three versions in force at different times (a legend-revision doc, plus a superseded `hard-perdiem-v2`). I didn't open the revision doc directly, but the row I used states "In force from 2026-01-01" with no end date, and today is 2026-09-20, so it's current — I relied on that inline note rather than cross-checking the revision legend, which is the one place I could have gone wrong if the dates hadn't lined up so cleanly. The three lookups (grade/band/stay) all landed on exact matches — "junior analyst," "Dhaka," and "eight nights" are each listed verbatim in their legend tables, so there was no need to fall back to "nearest entry above" reasoning. The row itself bundles lodging, meals, receipt threshold, and incidentals together, which is convenient but easy to misread if you're only scanning for one figure — worth double-checking you're citing "Lodging, per night" and not "Meals, per day" for the hotel cap.
