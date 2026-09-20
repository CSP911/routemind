1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body

2. **Answer**
Lodging (hotel) cap: 255 USD per night. Receipt required for any spend above 44 USD (the receipt threshold). This is under the current overseas per-diem table, in force from 2026-01-01.

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s1/body

4. **Notes**
The expense area's table listing flags up front that overseas per-diem has three versions in force over different date ranges (a superseded v2 body and legend-revision file sit right next to the current table at the /v1/regions/expense level). It would have been easy to grab the wrong version's figures. I picked `sec-hard-perdiem` because its description explicitly says "THE CURRENT ... TABLE, in force from 2026-01-01," and today's date (2026-09-20) falls inside that window, so no need to open the superseded `hard-perdiem-v2` or `overseas-rates` bodies. The row address itself directly encoded grade/band/stay (g3-band-b3-stay-s1), so no legend lookup was needed to translate the question's inputs — they were already given as codes, not job titles or city names.
