1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body
```

2. **Answer**
For grade G2, band B4, stay S1 (current table, in force since 2026-01-01):
- Lodging (hotel), per night: 207 USD
- Receipt threshold: 49 USD — a receipt must be kept/attached above this amount.

(Also on this row, though not asked: meals 89 USD/day, incidentals 18 USD/day.)

3. **Source**
- /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s1/body

4. **Notes**
The grade/band/stay codes were given directly in the question (G2, B4, S1), so the legend files (hard-perdiem-legend-grade/band/stay) weren't needed to translate job title/destination/trip length into codes — the row address could be built straight from the codes printed in the sec-hard-perdiem table listing. The expense area's table blurb flags that overseas per-diem has three versions (current, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and `overseas-rates` before that) and that the older ones are superseded; today's date (2026-09-20) falls under the current table (effective from 2026-01-01), so no ambiguity there, but it would have been easy to grab a stale rate from `hard-perdiem-v2` if the "current" table hadn't been so clearly labeled. Nothing else about the walk was confusing — the row existed exactly as named, no interpolation required.
