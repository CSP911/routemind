1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3/body
```

2. **Answer**
For a managing director staying 8 nights in Tokyo (grade G4, band B1, stay S3), the nightly lodging cap is **295 USD**. Any spend above the **36 USD** receipt threshold requires a receipt.

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3/body (lodging cap and receipt threshold)

4. **Notes**
The expense region table flagged that overseas per-diem has three versions (a legend-revision warning) and listed both a superseded v2 table and the current one (`sec-hard-perdiem`, in force from 2026-01-01). Today's date (2026-09-20) falls under the current version, so no ambiguity there, but it would be easy to grab the wrong table if you didn't notice the revision warning first. The three legends (grade, band, stay) each map plain-language inputs to row codes and explicitly state they are "the only place the mapping is written down" — skipping any one of them makes it impossible to construct the correct row address. "Eight nights" matched an exact legend entry (stay S3), so no nearest-value judgment call was needed. The question asked only about the hotel/lodging figure and the receipt threshold, both of which are on this one row; the meal and incidentals figures on the same row were not asked for and are omitted.
