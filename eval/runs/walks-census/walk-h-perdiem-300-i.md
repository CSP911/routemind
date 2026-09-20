1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body

2. **Answer**
Lodging cap: 287 USD per night. Receipt required for any spend above 30 USD (the row's receipt threshold).

3. **Source**
/v1/nodes/sec-hard-perdiem (table, current since 2026-01-01)
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s1/body

4. **Notes**
The expense area table flags up front that overseas per-diem has three superseding versions (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), so it would be easy to grab an old row by accident — I stuck with `sec-hard-perdiem` since it's explicitly the one in force from 2026-01-01 and today is 2026-09-20. The row itself is indexed only by codes (G/B/S), not by job title, city, or trip length, so the three legend lookups (grade, band, stay) are mandatory rather than optional — there's no way to guess the row address without them, matching the tool's "never construct an address" rule. Mapping was direct: managing director → G4, Tokyo → B1, one night → S1, no nearest-match judgment calls needed. The row conveniently states both the nightly lodging cap and its own receipt threshold together, so no separate trip to the general `/v1/nodes/evidence` table was needed for this specific figure.
