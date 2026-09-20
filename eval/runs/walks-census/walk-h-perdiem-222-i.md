1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
```

2. **Answer**
A department head on an 8-night trip to Jakarta (grade G3, band B3, stay S3) may put **263 USD per night** on the hotel. The receipt threshold for this row is **50 USD** — above that amount a receipt/evidence is required.

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → B3)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → S3)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body (the figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms current table applies for 2026-09-20)

4. **Notes**
- The expense region table explicitly warns that overseas per-diem has three superseded/current versions, and the region's own listing flags the current table only applies from 2026-01-01 — easy to grab the wrong row (`hard-perdiem-v2` or `overseas-rates`) if the date isn't checked. Today (2026-09-20) is safely inside the current table's range, and I confirmed this deliberately via the revision legend rather than assuming "newest is always right."
- "Eight nights" maps exactly onto the S3 stay-band legend entry ("eight nights → stay S3"), so no rounding/nearest-neighbor judgment call was needed there — a stroke of luck, since other trip lengths (e.g. 6 nights) would have forced a "nearest entry above it" decision per the legend's own instructions.
- The per-diem row bundles receipt threshold alongside lodging/meals/incidentals, so once the three qualifiers (grade/band/stay) are resolved, one file read gives the complete answer — no separate trip to the generic `/v1/nodes/evidence` table was needed for this question.
- Did not need to consult `sec-trip-days-versus-allowance-days`, since the question asks about the nightly rate for a stay-length band, not about reconciling trip days vs. paid allowance days.
