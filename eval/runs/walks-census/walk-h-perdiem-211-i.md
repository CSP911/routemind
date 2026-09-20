1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body

2. **Answer**
For a department head on a 4-night trip to Singapore, under the current overseas per-diem table (in force from 2026-01-01): lodging cap is 243 USD per night, and the receipt threshold is 38 USD (receipts required above that amount). (Also on this row, though not asked: meals 75 USD/day, incidentals 15 USD/day.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed today's date, 2026-09-20, falls under the current table, not the two superseded versions)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s2/body (final figures)

4. **Notes**
This subject has three overlapping versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) and the legend-revision page explicitly warns that grabbing the newest without checking the date is wrong for anything before 2026-01-01 — easy trap if you skip straight to `sec-hard-perdiem` without checking. Today's date (2026-09-20) does fall in the current table's range, so this was not actually a case where the trap bites, but it was worth confirming rather than assuming. The three legends (grade/band/stay) each warn that an unlisted input should map to "the nearest entry above it" — none of the three inputs here (department head, Singapore, four nights) were ambiguous or needed that fallback, all matched exactly. The row body's "If the figures are exceeded" section (unrequested) describes a further approval path for excess spend, not part of what was asked.
