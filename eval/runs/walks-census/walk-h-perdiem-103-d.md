1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body

2. **Answer**
Lodging (hotel) cap: 171 USD per night. Receipt threshold: 31 USD — spend above this amount requires a receipt to be kept.
(Also on this row, though not asked: meals 62 USD/day, incidentals 12 USD/day.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body

4. **Notes**
The expense region's table listing flags upfront that overseas per-diem has THREE versions covering different date ranges (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, and the current `sec-hard-perdiem` in force from 2026-01-01). It would have been easy to grab the wrong version — the table listing even surfaces the superseded `hard-perdiem-v2` file directly alongside the current one at the region level, before you drill into the actual current table. Since today's date (2026-09-20) falls inside the current table's validity window, `sec-hard-perdiem` was the correct one to use, and its row for G2/B1/S4 gave both figures directly with no legend lookups needed since the grade/band/stay codes were given exactly in the question.
