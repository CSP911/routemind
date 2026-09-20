1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s2/body

2. **Answer**:
For grade G2, band B4, stay S2 (current overseas per-diem table, in force from 2026-01-01):
- Lodging cap, per night: 211 USD
- Receipt required above: 52 USD (the receipt threshold)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s2/body

4. **Notes**:
The question gave grade/band/stay as codes (G2, B4, S2) directly, so there was no need to consult
the legend files (`hard-perdiem-legend-grade`, `hard-perdiem-legend-band`, `hard-perdiem-legend-stay`)
that translate job title/destination city/trip length into those codes — this walk skipped straight
to the row.

The one place this could have gone wrong: the `expense` table lists three versions of the overseas
per-diem (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), with an explicit
warning node (`hard-perdiem-legend-revision`) about picking the right one. Today's date (2026-09-20)
falls after the current table's 2026-01-01 start, so `sec-hard-perdiem` is the correct source and the
other two are superseded — but a careless read of the table listing (which sorts alphabetically, not
chronologically) could easily have grabbed `hard-perdiem-v2` by mistake since it appears earlier in
the listing. Also note the row returns four figures (lodging, meals, receipt threshold, incidentals);
the question only asked about hotel/night and the receipt threshold, so meals and incidentals were
left out of the answer deliberately, not missed.
