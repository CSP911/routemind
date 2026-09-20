1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body

2. **Answer**:
Lodging cap per night: 163 USD.
Receipt required above: 25 USD (receipt threshold).
(For context, also in this row: meals 52 USD/day, incidentals 10 USD/day.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body

4. **Notes**:
The expense area's table listing flags upfront that overseas per-diem has THREE versions with overlapping documents (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`) — it would be easy to grab an old file (e.g. `hard-perdiem-v2` from the region-level listing) by mistake since it's surfaced right alongside the current table. Went straight to `sec-hard-perdiem`, which its own description confirms is in force from 2026-01-01, and today (2026-09-20) falls within that range, so no need to open the superseded versions or the revision-legend file at all. The row address itself directly encoded the grade/band/stay combination (g2-band-b1-stay-s2), so no legend lookups were needed either — the qualifiers in the question mapped straight onto the address.
