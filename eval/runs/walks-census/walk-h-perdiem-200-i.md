1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body
```

2. **Answer**
Lodging cap: 223 USD per night. Receipt threshold: above 26 USD a receipt must be kept.
(Department head → grade G3; Tokyo → band B1; one night → stay S1.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (department head = G3)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo = B1)
- /v1/nodes/hard-perdiem-legend-stay/body (one night = S1)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s1/body (223 USD lodging, 26 USD receipt threshold)

4. **Notes**
The expense region table flags three overlapping versions of the overseas per-diem (a legend-revision warning node, a superseded `hard-perdiem-v2`, and the current `sec-hard-perdiem`). It would have been easy to grab the superseded v2 table by mistake since it sits right next to the current one in the listing with a similarly-worded description — the "in force from 2026-01-01" / "SUPERSEDED" labels in the table's own WHY column were the only thing that disambiguated it, and today (2026-09-20) falls inside the current table's validity window. The three legends (grade, band, stay) are not optional reading — the per-diem rows are indexed purely by codes (G3/B1/S1) with no plain-English fallback, so skipping any one of the three legends would have made it impossible to pick the right row out of the 64 listed.
