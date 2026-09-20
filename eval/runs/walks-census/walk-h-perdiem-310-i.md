1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body

2. **Answer**
Lodging cap: 303 USD per night. Receipt required above: 39 USD (the row's receipt threshold). This applies to a managing director (grade G4), traveling to Singapore (band B2), staying one night (stay S1), under the per-diem table in force since 2026-01-01.

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s1/body

4. **Notes**
The expense area table flagged up front that overseas per-diem has three superseded versions (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, `overseas-rates`); it would have been easy to grab figures from the wrong era. I went straight for `sec-hard-perdiem`, which is explicitly labeled as the table in force from 2026-01-01, and today is 2026-09-20, so it's current — didn't need to open the superseded ones. The three legends (grade, band, stay) are mandatory reading before touching a row: the row addresses are built from opaque codes (g4/b2/s1) that only the legends decode, and the tool warns never to construct an address yourself, so skipping straight to a guessed row address would have been the wrong move even if the guess happened to be right. No ambiguity in the mappings themselves — "managing director," "Singapore," and "one night" each hit an exact row in their legend tables, no nearest-match judgment calls needed.
