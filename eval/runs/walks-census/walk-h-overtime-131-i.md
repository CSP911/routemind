1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body

2. **Answer**
Multiplier: 2.07x. Rounding: minutes are taken to the nearest 20 minutes.
(A Saturday = day D2, eleven hours = hours H4, out at a client's office = place P2. This row is in force from 2026-01-01, current as of today 2026-09-20.)

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p2/body

4. **Notes**
The overtime table under /v1/regions/attendance has three superseded revisions (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime`, in force from 2026-01-01) all sitting side by side in the listing — easy to grab a row from the wrong version if you don't check the "in force" note. I went straight for `sec-hard-overtime` since today's date (2026-09-20) falls in its range, and the row itself confirmed that with its own "In force from 2026-01-01" footer.
The three legends (day/hours/place) each warn that theirs is "the only place the mapping is written down" and that the row addresses don't repeat the plain-language description — so all three had to be read before the row address (d2-h4-p2) could even be constructed. Nothing in the question was ambiguous against the legends: "a Saturday," "eleven hours," and "out at a client's office" each matched an exact legend entry, no nearest-neighbor guessing needed.
