1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body

2. **Answer**:
Lodging (hotel) cap: 111 USD per night. Receipt threshold: 27 USD — above that amount a receipt must be kept. (For context, this row also lists meals at 52 USD/day and incidentals at 10 USD/day.) This is the current table, in force from 2026-01-01.

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body

4. **Notes**:
The expense area's table listing flagged up front that overseas per-diem has three superseded versions (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, `overseas-rates` vs. the current `sec-hard-perdiem`), which made me pause and check the date — today is 2026-09-20, well inside the "in force from 2026-01-01" current table, so no ambiguity there. The grade/band/stay codes (G1, B2, S1) were given directly in the question, so I didn't need to open the legend files to translate a job title, city, or trip length into codes — I went straight to the matching row address in the sec-hard-perdiem listing, which was printed verbatim. No detours or wrong turns on this one.
