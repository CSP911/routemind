1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body

2. **Answer**
Lodging (hotel) cap: 311 USD per night.
Receipt required above: 45 USD (the receipt threshold).
(For context, also in this row: meals 89 USD/day, incidentals 18 USD/day — not asked but part of the same row.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body

4. **Notes**
The expense area table flagged up front that overseas per-diem has three versions in force over different date ranges (`sec-hard-perdiem` current since 2026-01-01, `hard-perdiem-v2` superseded 2024-07-01 to 2025-12-31, and an older `overseas-rates` before that). It would have been easy to grab a superseded table by mistake — I picked `sec-hard-perdiem` because today's date (2026-09-20) falls inside its "in force from 2026-01-01" window, and the row body itself reconfirmed that date range. Grade/band/stay were given directly in the question (G4, B2, S3) so I didn't need the legend files to translate a job title or destination city into codes — went straight to the matching row address in the 64-row index.
