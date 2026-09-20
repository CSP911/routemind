1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body
```

2. **Answer**
Lodging (hotel) cap: 315 USD per night.
Receipt required above: 48 USD (the receipt threshold).
(For context, same row also gives meals at 94 USD/day and incidentals at 19 USD/day, but only lodging and receipt threshold were asked.)

3. **Source**
- /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body

4. **Notes**
The expense area table listed three versions of the overseas per-diem (a legend-revision doc, a superseded `hard-perdiem-v2`, and the current `sec-hard-perdiem`). It would have been easy to grab the wrong one — `hard-perdiem-v2` sits right next to the current table in the listing and its description doesn't loudly say "superseded" until you read closely. The `sec-hard-perdiem` table description explicitly states it's "in force from 2026-01-01," which matches today's date (2026-09-20), so I used that one and didn't need to open the legend-revision doc at all. The grade/band/stay row address was fully spelled out in the table listing (`hard-perdiem-row-grade-g4-band-b2-stay-s4`), so no lookup via the grade/band/stay legends was needed since the codes were already given in the question.
