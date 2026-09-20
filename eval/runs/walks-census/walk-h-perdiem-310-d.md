1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body

2. **Answer**
Lodging cap: 303 USD per night. Receipt required above 39 USD (the receipt threshold).
(For context, the same row also lists meals at 79 USD/day and incidentals at 16 USD/day, but the question only asked about the hotel and the receipt threshold.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body

4. **Notes**
The grade/band/stay codes (G4, B2, S1) were given directly in the question, so no legend lookup was needed to resolve them — the row address was fully determined from the table listing under /v1/nodes/sec-hard-perdiem, no guessing involved. The main risk here was version confusion: the expense area lists three per-diem documents (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), and a superseded 2024-07-01–2025-12-31 version (`hard-perdiem-v2`) is still present in the table. Today's date (2026-09-20) falls under the current table (in force since 2026-01-01), which the row body itself confirms ("In force from 2026-01-01"), so I used that one and did not need to open the legend-revision doc. Worth flagging: "receipt threshold" here means the amount above which a receipt must be kept/attached, not a spending cap — the question's phrasing could be misread as asking for a second dollar limit on the hotel itself, but the table has only one lodging figure (303 USD/night) plus the one receipt threshold (39 USD) that applies across the whole row, not specifically to lodging.
