1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body

2. **Answer**
For a managing director on a three-week trip to Singapore, in force from 2026-01-01 (today, 2026-09-20, falls under this version):
- Hotel (lodging), per night: 315 USD
- Receipt required above: 48 USD

(For context, not asked but on the same row: meals 94 USD/day, incidentals 19 USD/day.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions applies to today's date)
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body (final figures)

4. **Notes**
The overseas per-diem subject has three separate versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) covering different date ranges, and the legend-revision page warns explicitly that the oldest one never says it was superseded — reaching for the newest table without checking today's date against the ranges would have been the natural mistake here. Since today is 2026-09-20, the current table (`sec-hard-perdiem`, in force from 2026-01-01) was the right one, but this only became clear after reading the revision-legend page.

The per-diem row is indexed by three codes (grade/band/stay) that have to be looked up separately via three legend files — none of the plain-language terms in the question ("managing director," "Singapore," "three weeks") appear directly in the row table, so skipping any one legend would have made the address unguessable. All three mapped cleanly with no ambiguity (managing director = G4, Singapore = B2, three weeks = S4).

"Receipt threshold" on the row is worded exactly like the question's "above what amount do I have to keep the receipt," so I used it directly rather than also opening the general `/v1/nodes/evidence` table — that table looked like it would cover evidence rules for other categories of spend, and the per-diem row's own field already answers the question asked for this specific trip.
