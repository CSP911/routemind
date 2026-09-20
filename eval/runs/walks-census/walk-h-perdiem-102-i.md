1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
For a team manager (grade G2), Tokyo (band B1), 8 nights (stay S3) — under the per-diem table in force from 2026-01-01:
- Hotel/lodging cap: 167 USD per night
- Receipt required above: 28 USD (the receipt threshold)
(For reference, this row also lists meals at 57 USD/day and incidentals at 11 USD/day, though not asked.)

3. **Source**:
- /v1/regions/expense (navigation)
- /v1/nodes/sec-hard-perdiem (navigation)
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → G2)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → B1)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → S3)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s3/body (the figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms this is the correct version for 2026-09-20)

4. **Notes**:
The stay legend maps "eight nights" exactly to S3 — no rounding or nearest-match judgment needed, which was a relief since the legend text warns to take the nearest entry when a value isn't listed (this one was listed exactly).
The trickiest part was date-sensitivity: the expense area table flagged upfront that overseas per-diem has three superseded versions, and the legend-revision doc explicitly warns not to reach for the newest version by default — a 2025-dated question would need `hard-perdiem-v2`, not the current table. Today (2026-09-20) is safely inside the 2026-01-01-onwards current table (`sec-hard-perdiem`), so no correction was needed, but this is exactly the kind of thing that's easy to get wrong without checking the revision doc explicitly.
The "receipt threshold" figure sits inside the same per-diem row as lodging/meals/incidentals rather than in the general `evidence` table — I initially expected the receipt requirement to be a flat company-wide number from `/v1/nodes/evidence`, but this per-diem row has its own threshold (28 USD) specific to this grade/band/stay combination, so I used that rather than looking further.
