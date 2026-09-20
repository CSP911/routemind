1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body
```

2. **Answer**
Lodging cap: 319 USD per night. Receipt required for any spend above 48 USD.
(Managing director → grade G4; Jakarta → band B3; one night → stay S1, under the overseas per-diem table in force since 2026-01-01.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirms which per-diem version applies to a 2026-09-20 date)
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → G4)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → B3)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → S1)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body (lodging cap and receipt threshold)

4. **Notes**
The expense area's table listing flags up front that overseas per-diem has three versions in force over different date ranges, and a dedicated warning doc (hard-perdiem-legend-revision) spells out that reaching for the newest table is wrong unless the question's date actually falls in it. Today's date (2026-09-20) is safely inside the current table's range (2026-01-01 onward), so this wasn't a case where the trap actually bit, but skipping that check and jumping straight to `sec-hard-perdiem` would have been a guess rather than a verified choice — worth flagging since the walk deliberately routes through that ambiguity. The three qualifiers (grade/band/stay) each required a separate legend lookup rather than being guessable from the job title, city, and duration as given in the question; the legend files were the only place those mappings existed. The row itself already carries a receipt threshold, so no separate trip to the general evidence table was needed for this question.
