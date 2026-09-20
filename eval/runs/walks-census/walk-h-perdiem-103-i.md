1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body

2. **Answer**
Lodging cap: 171 USD per night. Receipt required above 31 USD (the receipt threshold). (For reference, the same row also gives meals at 62 USD/day and incidentals at 12 USD/day, though these weren't asked.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body (the figures)

4. **Notes**
- The expense region table flags up front that overseas per-diem has THREE versions in force at different dates (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`). It would be easy to grab an old version by mistake. I went straight for `sec-hard-perdiem`, which is explicitly labeled "in force from 2026-01-01" and today is 2026-09-20, so it's current; the row body also self-confirms this in its footer. Didn't need to open the revision-legend file separately since the table description and row footer already established currency, but a more cautious walk might read it too.
- "Three weeks" mapped exactly onto stay band S4 ("three weeks") in the legend — no rounding or nearest-match judgment call was needed, which was a relief since the legend's fallback instruction ("take the nearest entry above it") suggested I might have to guess.
- The three legends (grade/band/stay) must each be resolved before the specific row address can even be constructed; the row addresses are not discoverable by guessing — I had to read the table listing of `sec-hard-perdiem` first to see the naming pattern (`hard-perdiem-row-grade-gX-band-bY-stay-sZ`) confirmed by the legends' codes.
