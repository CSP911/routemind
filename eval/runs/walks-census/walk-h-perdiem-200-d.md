1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body
```

2. **Answer**
For grade G3, band B1, stay S1 (in force from 2026-01-01, current as of 2026-09-20):
- Lodging cap: 223 USD per night
- Receipt threshold: 26 USD — a receipt must be kept for any spend above this amount

3. **Source**
- /v1/nodes/sec-hard-perdiem (table, confirmed this is the current table, in force from 2026-01-01)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body (figures)

4. **Notes**
The expense area's table listing flags up front that overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), which is the one place this walk could easily go wrong — picking the wrong version by address-guessing or by following the first per-diem-looking hit. The `sec-hard-perdiem` table's own description states plainly it's "in force from 2026-01-01," and today is 2026-09-20, so no ambiguity once you're at the right table. The row address itself directly named the requested grade/band/stay combination (`hard-perdiem-row-grade-g3-band-b1-stay-s1`), so no legend lookups (grade/band/stay) were needed — the question already gave the codes. Did not open the superseded `hard-perdiem-v2` or `overseas-rates` bodies since the row body itself restates the version lineage and confirms currency.
