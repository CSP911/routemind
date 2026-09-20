1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**: Lodging cap is 215 USD per night. The receipt threshold is 55 USD — above that amount a receipt must be kept as evidence. (This row also carries a meal allowance of 99 USD/day and incidentals of 20 USD/day, not asked for but part of the same row.) This is for a team manager (grade G2) traveling to Dhaka (band B4) for eight nights (stay S3), under the per-diem table in force from 2026-01-01, which covers today's date of 2026-09-20.

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body
/v1/nodes/hard-perdiem-legend-revision/body (used to confirm table version validity for today's date)

4. **Notes**: The per-diem area has three superseded/current versions of the same subject (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the revision legend explicitly warns that reaching for the newest is wrong for dates before 2026-01-01 — an easy trap if the walk hadn't checked the date against the table's effective range. Also, none of the three qualifiers (grade/band/stay) are guessable from the question's wording alone — "team manager," "Dhaka," and "eight nights" only resolve to G2/B4/S3 by reading three separate legend files first; the 64-row table gives no shortcut and does not repeat the mapping anywhere else. Nothing else here was ambiguous — the row cleanly named both the lodging cap and the receipt threshold in one document.
