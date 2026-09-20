1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body

2. **Answer**
For a team manager (grade G2) on a three-week trip (stay S4) to Dhaka (band B4), under the per-diem table in force since 2026-01-01:
- Lodging cap: 219 USD per night
- Receipt required above: 58 USD (the receipt threshold — spend above this amount needs a receipt as evidence)

(For context, the same row also lists meals at 104 USD/day and incidentals at 21 USD/day, though those weren't asked.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → G2)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → B4)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → S4)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body (the figures: 219 USD lodging, 58 USD receipt threshold)

4. **Notes**
The expense area table flags up front that overseas per-diem has three superseded/superseding versions living side by side, and that the oldest one "says nothing at all about having been replaced" — so it would be easy to grab the wrong row (`overseas-rates` or `hard-perdiem-v2`) without ever seeing an error. Reading `hard-perdiem-legend-revision` before touching the numbers table was the thing that avoided that; today's date (2026-09-20) falls after 2026-01-01, so `sec-hard-perdiem` is correct. Also worth flagging: "three weeks" maps exactly to the S4 legend entry (no rounding/nearest-match judgment call needed there), unlike the grade and band mappings which are drop-in matches too in this case (team manager and Dhaka are both listed literally). No ambiguity remained by the time the row was fetched.
