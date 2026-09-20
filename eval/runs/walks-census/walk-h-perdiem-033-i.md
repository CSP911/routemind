1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body

2. **Answer**
Lodging cap: 155 USD per night. Receipt threshold: 54 USD — spend above this amount requires a receipt as evidence.
(Junior analyst = grade G1; Dhaka = band B4; three weeks = stay S4. This row also gives meals at 95 USD/day and incidentals at 19 USD/day, not asked for but adjacent.)

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s4/body

4. **Notes**
The expense area lists three overseas per-diem versions (a legend-revision warning file, a superseded v2 file, and the current `sec-hard-perdiem` table). It would be easy to grab the older superseded file by mistake since it sits right next to the current one in the table listing — the current table is explicitly marked "in force from 2026-01-01" and today is 2026-09-20, so `sec-hard-perdiem` is the correct one. The per-diem table itself doesn't spell out grade/band/stay in the row list — you have to open the three separate legend files to translate "junior analyst," "Dhaka," and "three weeks" into G1/B4/S4 before the row address can be built (well, selected — addresses are never hand-constructed, only chosen from what's printed). The receipt threshold turned out to live inside the same per-diem row as the lodging cap, so no separate trip to the general `/v1/nodes/evidence` table was needed — that could easily have been an extra unnecessary hop.
