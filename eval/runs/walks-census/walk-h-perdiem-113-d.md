1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body

2. **Answer**:
Lodging cap: 187 USD per night. Receipt threshold: 40 USD — spend above that amount requires a receipt to be kept. (Also on this row: meals 76 USD/day, incidentals 15 USD/day.) This is the current table, in force from 2026-01-01, which covers today's date (2026-09-20).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body

4. **Notes**:
The expense area's table listing flags that overseas per-diem has THREE versions with different dates (`overseas-rates`, `hard-perdiem-v2` superseded 2024-07-01 to 2025-12-31, and the current `sec-hard-perdiem` table from 2026-01-01) — easy to grab a superseded row by mistake if you don't check which table you're in. I went straight to `sec-hard-perdiem` since it was explicitly labeled current and its date range covers today, and confirmed the row itself restates "In force from 2026-01-01" with pointers to the older versions, which matched. Grade/band/stay codes were given directly in the question, so I didn't need the legend files (`hard-perdiem-legend-grade/band/stay`) to translate a job title, city, or trip length into a code — but if the codes hadn't been pre-supplied, skipping those legends would have been a mistake.
