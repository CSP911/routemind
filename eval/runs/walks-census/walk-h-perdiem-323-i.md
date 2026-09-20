1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body

2. **Answer**:
Lodging cap: 331 USD per night. Receipt required above: 57 USD (the receipt threshold).
(For context, same row also gives meals 108 USD/day and incidentals 22 USD/day, in force from 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established which of the three per-diem versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body (the figures)

4. **Notes**:
The expense area lists three per-diem documents (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) with no obvious cue in their table listing about which is current for a given date — the legend-revision file explicitly warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest document says nothing about being superseded. Today's date (2026-09-20) falls under the current table, but this was the one place a careless walk could have gone wrong: grabbing `hard-perdiem-v2` by habit, or not checking the revision doc at all. Otherwise the walk was clean — "three weeks" mapped exactly to the S4 legend row with no rounding judgment needed, unlike the band/grade legends which explicitly allow for nearest-entry approximation if the input isn't listed verbatim.
