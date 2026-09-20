1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 311 USD per night. Receipt required above 45 USD (the receipt threshold).
(Managing director → grade G4; Singapore → band B2; eight nights → stay S3; this is the table in force from 2026-01-01, current as of today, 2026-09-20.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (mapped "managing director" to grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (mapped "Singapore" to band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (mapped "eight nights" to stay S3)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body (the figures: 311 USD lodging, 45 USD receipt threshold)
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed the current table, not the superseded v2 or overseas-rates, applies to a 2026-09-20 question)

4. **Notes**:
The expense area lists three per-diem documents at once — the current table (`sec-hard-perdiem`), a superseded version (`hard-perdiem-v2`), and a legend-revision warning — with no date filter, so it's easy to grab the wrong one if you don't check the revision note. The revision note makes clear the date on the question decides the version, and specifically warns that the oldest version never says it was replaced, so reaching for the first match found would be wrong for older questions. Here the question is dated 2026-09-20, safely inside the current (2026-01-01 onwards) table, so no ambiguity in this case — but it was worth confirming rather than assuming "current" is always right.

The per-diem row bundles four figures (lodging, meals, receipt threshold, incidentals) under one address, and the table row description text is truncated ("...the re…") which could be misread as unrelated to "receipt" — had to open the row body to see "Receipt threshold" spelled out. The three-qualifier indexing (grade/band/stay) requires three separate legend lookups before the row address can even be constructed correctly from the walk (each legend explicitly says "never build one," so all three had to be opened rather than guessed).
