1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body

2. **Answer**
For a department head, Dhaka, 8 nights (grade G3, band B4, stay S3): the nightly lodging cap is 279 USD. A receipt is required above 59 USD (the receipt threshold for this row).

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
/v1/nodes/hard-perdiem-legend-band/body (Dhaka → B4)
/v1/nodes/hard-perdiem-legend-stay/body (8 nights → S3)
/v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body (lodging cap and receipt threshold figures)

4. **Notes**
The expense region's table description flags that overseas per-diem has three superseded versions layered on top of each other (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, `overseas-rates` vs. the current `sec-hard-perdiem`); it would be easy to grab an old table by name-matching alone. I picked `sec-hard-perdiem` because its own listing states it's "in force from 2026-01-01" and today is 2026-09-20, and the row body itself reconfirms that in-force date and points to the two older versions rather than silently using one of them. The three legends (grade/band/stay) are mandatory reads — the row addresses are coded (g3-b4-s3) and not guessable from the plain-language question, so skipping any one of them risks picking the wrong row. "Eight nights" matched the S3 legend entry exactly ("eight nights"), so no rounding judgment was needed there, unlike the grade/band mappings which are closer to direct lookups anyway (department head and Dhaka are both listed verbatim). The receipt threshold turned out to live inside the same per-diem row rather than in the separate `/v1/nodes/evidence` table, which I had expected to need — worth noting in case that's not always the case for other grade/band/stay combinations.
