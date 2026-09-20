1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body

2. Answer
Lodging (hotel) cap: 323 USD per night.
Receipt threshold: above 51 USD a receipt must be kept.
(For context, this row also gives meals at 98 USD/day and incidentals at 20 USD/day, though those weren't asked for.)

3. Source
/v1/regions/expense
/v1/nodes/sec-hard-perdiem
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body

4. Notes
The expense area table flags up front that overseas per-diem has three versions (current since 2026-01-01, a superseded 2024-07-01 version, and an older one before that) — easy to grab a stale row if you don't notice the warning and check today's date (2026-09-20) falls in the current version's range. The three qualifiers (grade, band, stay length) are each resolved through a separate legend file rather than being guessable from the question's wording — "managing director" only maps to "G4" via the grade legend, "Jakarta" to "B3" via the band legend, and "four nights" to "S2" via the stay legend; none of these codes are inferable without reading the legends first. Nothing here was ambiguous once the legends were read; the only near-miss was almost opening the older superseded per-diem files (hard-perdiem-v2 or overseas-rates) instead of sec-hard-perdiem.
