1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body

2. **Answer**
Lodging cap: 259 USD per night. Receipt required above: 47 USD (receipt threshold).
(For context, also in this row: meals 89 USD/day, incidentals 18 USD/day — not asked but same row.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body

4. **Notes**
The expense area table flags that overseas per-diem has THREE versions in force at different times (`overseas-rates`, `hard-perdiem-v2` superseded 2024-07-01–2025-12-31, and the current `sec-hard-perdiem` table in force since 2026-01-01). Today's date (2026-09-20) falls under the current table, so `sec-hard-perdiem` was the correct one to use — but it would have been easy to grab the superseded `hard-perdiem-v2` node instead since it's listed right next to the current one at the region level with similarly-worded blurbs. The row itself confirms this by naming its own effective date and pointing back to the older versions, which was a useful cross-check that I had the right vintage. Otherwise the walk was direct: grade/band/stay is a straightforward three-key lookup and the row address was printed verbatim by the table listing, so no address had to be inferred or built.
