1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body

2. **Answer**
Hotel (lodging) cap: 283 USD per night.
Receipt required above: 62 USD.
(For context, this row also gives: meals 113 USD/day, incidentals 23 USD/day.)

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s4/body

4. **Notes**
All three lookups (grade, band, stay) matched an exact legend row — no nearest-entry fallback was needed: "department head" → grade G3, "Dhaka" → band B4, "three weeks" → stay S4. The expense region table flags that overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem` in force from 2026-01-01); today's date (2026-09-20) falls under the current table, so I did not need to check the older versions, but it would be easy to grab a stale row by accident if the region table's warning were skipped. The row is indexed strictly by the three legend codes and gives no separate general "receipt threshold" elsewhere — I took the 62 USD figure printed directly in the matched row rather than searching further, since it's presented as part of the same per-diem entry.
