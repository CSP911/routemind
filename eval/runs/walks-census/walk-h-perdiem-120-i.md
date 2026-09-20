1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body

2. **Answer**
For a team manager, one night in Jakarta (grade G2, band B3, stay S1), under the overseas per-diem table in force from 2026-01-01: lodging cap is 191 USD per night. A receipt must be kept above 40 USD (the receipt threshold).

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body (confirms which of the three per-diem versions applies to today's date, 2026-09-20)
/v1/nodes/hard-perdiem-legend-grade/body (team manager → G2)
/v1/nodes/hard-perdiem-legend-band/body (Jakarta → B3)
/v1/nodes/hard-perdiem-legend-stay/body (one night → S1)
/v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s1/body (the figures: 191 USD lodging/night, 40 USD receipt threshold)

4. **Notes**
The expense area lists three separate per-diem documents (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) with no obvious warning at the region-table level that they overlap or supersede each other — the table listing even flags the older bands as "still here and superseded," which could tempt picking the wrong one on a skim. The `hard-perdiem-legend-revision` document is what actually resolves this: it states the oldest version never claims to have been replaced, so date-checking against today (2026-09-20) is mandatory rather than optional. That put the question firmly in `sec-hard-perdiem` (2026-01-01 onward), not the other two.
Also worth flagging: the row page lists "Receipt threshold" as one figure (40 USD) rather than a hotel-specific threshold — I read it as the receipt threshold applicable to this per-diem row generally (which is what the question asked "above what amount do I have to keep the receipt"), not a lodging-only rule. Nothing in the row separates a hotel-specific receipt rule from a general one, so I did not invent a distinction that isn't in the source.
