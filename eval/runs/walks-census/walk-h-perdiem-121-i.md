1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body
```

2. **Answer**
Lodging (hotel) cap: 195 USD per night.
Receipt threshold: above 43 USD a receipt must be kept.
(This is for grade G2 — team manager — band B3 — Jakarta — stay S2 — four nights, under the per-diem table in force from 2026-01-01, which applies since today is 2026-09-20.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions covers today's date)
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → G2)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → B3)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → S2)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s2/body (the figures: 195 USD lodging/night, 43 USD receipt threshold)

4. **Notes**
- The expense area table flags up front that overseas per-diem has three superseded/current versions and warns that reaching for the newest is wrong for dates before 2026-01-01 — worth checking explicitly rather than assuming the current table applied, even though today's date (2026-09-20) does fall under the current one (`sec-hard-perdiem`, in force from 2026-01-01).
- The three qualifiers (grade, band, stay) are each in a separate legend file and none of the per-diem row files repeat the plain-language inputs — "team manager," "Jakarta," "four nights" all had to be translated via their respective legend tables before the row address could be built. It would have been easy to guess a row address directly from the question's terms; the tool's "never build one" instruction and the presence of three separate legend files made clear that translation was mandatory, not optional.
- No ambiguity in the mapping itself: team manager → G2, Jakarta → B3, four nights → S2 are all exact matches in their legends, not nearest-value approximations.
