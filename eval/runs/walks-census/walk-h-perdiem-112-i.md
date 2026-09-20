1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 183 USD per night. Receipt threshold: 37 USD — above that amount a receipt must be kept as evidence (this row also lists meals at 71 USD/day and incidentals at 14 USD/day, not asked for here but part of the same row).
This uses grade G2 (team manager), band B2 (Singapore), stay S3 (eight nights), current table in force since 2026-01-01, which covers today's date (2026-09-20).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s3/body (lodging cap and receipt threshold figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms which of the three per-diem versions applies to today's date)

4. **Notes**:
The expense region table flags up front that overseas per-diem has three superseded/current versions, so before trusting the row values I checked the revision legend to make sure 2026-09-20 falls under the current `sec-hard-perdiem` table (it does — in force from 2026-01-01) rather than the superseded `hard-perdiem-v2` or `overseas-rates`. Easy to miss if you just grab the first "current table" table without checking the date against it.
The three legends (grade, band, stay) each say "if what you have is not listed, take the nearest entry above it" — none of that fuzzy-matching was needed here since "team manager", "Singapore", and "eight nights" all match a listed value exactly, but it's worth flagging that the stay legend's "eight nights" is an exact label match, not a rounded/nearest one — this row is a precise fit, not an approximation.
The row bundles four figures (lodging, meals, receipt threshold, incidentals); the question only asked about the hotel cap and receipt threshold, so I read all four but reported only the two asked for, noting the other two exist in the same row in case they're wanted later.
