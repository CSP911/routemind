1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body

2. **Answer**:
Lodging (hotel), per night: 267 USD.
Receipt threshold: 53 USD — above this amount the receipt must be kept.
(For context, also on this row: meals 99 USD/day, incidentals 20 USD/day, in force from 2026-01-01.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body

4. **Notes**:
The expense area's table listing flagged up front that overseas per-diem has three versions in force over different date ranges (a superseded v2 for 2024-07-01–2025-12-31, an older `overseas-rates`, and the current `sec-hard-perdiem` table from 2026-01-01). Today's date (2026-09-20) falls under the current table, so I went straight to `sec-hard-perdiem` and didn't need to open the revision-legend file — but it would have been easy to grab the wrong version if the date weren't already fixed for me. The grade/band/stay codes given in the question (G3/B3/S4) matched the row address exactly, so no legend lookup (grade/band/stay definitions) was needed either. Single row, no ambiguity once the current table was identified.
