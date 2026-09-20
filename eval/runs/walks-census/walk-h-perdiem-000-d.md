1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s1/body

2. **Answer**
Lodging (hotel) cap: 95 USD per night.
Receipt threshold: above 18 USD you must keep the receipt.
(For context, also in this row: meals 38 USD/day, incidentals 7 USD/day.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s1/body

4. **Notes**
The expense area's table listing flags upfront that overseas per-diem has THREE versions in force at different times (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-perdiem` for 2026-01-01 onward). It would have been easy to grab the wrong one — `hard-perdiem-v2` is listed right next to the current table in the expense region and looks just as authoritative at a glance. Today's date (2026-09-20) falls under the current table, so `sec-hard-perdiem` was the correct pick; the row's own footer confirms the 2026-01-01 effective date and cross-references the superseded versions, which matched. The G1/B1/S1 row was available directly by address once inside `sec-hard-perdiem`, so no legend lookups (grade/band/stay) were needed since the question already gave the codes explicitly.
