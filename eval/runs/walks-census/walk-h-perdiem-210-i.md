1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body

2. **Answer**
Hotel (lodging) cap: 239 USD per night. Receipt required above: 35 USD (the receipt threshold). This is for a department head (grade G3), Singapore (band B2), a one-night stay (stay S1), under the per-diem table in force from 2026-01-01.

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → B2)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → S1)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body (figures: 239 USD lodging, 35 USD receipt threshold)

4. **Notes**
The expense area table flagged up front that overseas per-diem has three versions in force over different date ranges (a superseded 2024-07-01–2025-12-31 version, `hard-perdiem-v2`, and an older `overseas-rates`), with a legend node (`hard-perdiem-legend-revision`) specifically warning about this. It was easy to grab a stale row by accident — I made sure to open `sec-hard-perdiem`, which is explicitly labeled as the table in force from 2026-01-01, matching today's date (2026-09-20), and did not touch the superseded nodes. The three legends (grade, band, stay) are separate small files rather than columns in the row table itself, so all three had to be resolved individually before the 64-row table could be narrowed to one address — skipping any one of them risks guessing the row address directly, which the tool explicitly warns against ("never build one"). The row itself bundles lodging, meals, receipt threshold, and incidentals together, so no separate "evidence" table lookup was needed for the receipt threshold — it's given right there in the same row as the hotel cap.
