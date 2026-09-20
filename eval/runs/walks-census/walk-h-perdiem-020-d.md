1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body
```

2. **Answer**
Lodging (hotel), per night: 127 USD.
Receipt required above: 36 USD.
(Also on this row, though not asked: meals 66 USD/day, incidentals 13 USD/day.)

3. **Source**
`/v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body`

4. **Notes**
The row for grade G1, band B3, stay S1 exists exactly as named, so no legend lookup (grade/band/stay definitions) was needed to resolve the codes — the question already gave them in RouteMind's own terms. The one place to be careful is the per-diem table's versioning: the region's own listing flags that overseas per-diem has three superseded/current versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), and the row itself repeats that it's "in force from 2026-01-01" with the prior version named `hard-perdiem-v2`. Today is 2026-09-20, so the current table is the right one — but it would be easy to grab a superseded per-diem row if not reading that footnote. The row bundles the receipt threshold together with the lodging/meal/incidental caps, so no separate lookup in the `evidence` table was needed for that half of the question.
