1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body
```

2. **Answer**
Lodging cap: 259 USD per night. Receipt is required for any hotel spend above 47 USD (the receipt threshold).

(For context, same row also gives meals at 89 USD/day and incidentals at 18 USD/day, but these were not asked for.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s2/body (the figures)

4. **Notes**
The expense region table flags up front that overseas per-diem has three superseded versions layered in the same area (`hard-perdiem-v2`, `overseas-rates`, and the current `sec-hard-perdiem` in force from 2026-01-01). It would be easy to grab an old rate table by mistake if you didn't read the region description carefully — the current table's own name doesn't shout "current," you have to notice the in-force date and compare it to today (2026-09-20), which falls inside the current version's range with no listed end date. None of the three legend mappings (grade/band/stay) were obvious from the question's wording alone — "department head" isn't a grade code, "Jakarta" isn't a band code, and "four nights" isn't a stay code, so all three had to be resolved via their dedicated legend files before the row address could even be constructed correctly. Getting any one of the three codes wrong (e.g. reading "four nights" as S3 instead of S2, or Jakarta as B2 like Singapore) would silently point to a different, wrong row with no error — worth double-checking against the legend tables exactly as printed.
