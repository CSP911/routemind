1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body

2. **Answer**:
For grade G1, band B3, stay S2 (current overseas per-diem table, in force from 2026-01-01):
- Lodging (hotel), per night: 131 USD
- Receipt threshold: 39 USD — a receipt must be kept for any spend above this amount.
(Also on this row, for context: Meals, per day: 71 USD; Incidentals, per day: 14 USD.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body

4. **Notes**:
The `/v1/regions/expense` table flagged that overseas per-diem has three superseded versions
(`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem` table effective
2026-01-01). It would have been easy to grab the wrong version if grepping by name alone — the
row itself confirms "In force from 2026-01-01," which covers today's date (2026-09-20), so no
need to open the legend-revision document separately. The grade/band/stay values (G1, B3, S2)
were given directly in the question, so the legend files (grade/band/stay) weren't needed —
skipping straight to the matching row was safe here, but in a question with role/city/duration
in plain words instead of codes, those legends would be required first.
