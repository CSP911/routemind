1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**
Lodging cap: 179 USD per night. Receipt threshold: 34 USD (above this amount, the receipt must be kept/attached; this also happens to equal the per-day incidentals rate). For context, meals are 66 USD/day and incidentals 13 USD/day under the same row, though not asked for directly. This is the current table, in force from 2026-01-01, and applies to today's date (2026-09-20).

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body (the figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms this table version is the one in force for today's date)

4. **Notes**
The main trap here is the three superseded versions of the per-diem table (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) — the region's table listing surfaces the two older ones right alongside the current one with no obvious visual demotion, and the oldest version "says nothing at all about having been replaced" per the revision-legend doc. It would be easy to grab a row from `hard-perdiem-v2` by habit or because it appeared first in a listing. I explicitly checked the revision legend after finding my answer to confirm 2026-09-20 falls under the current `sec-hard-perdiem` table, which it does.

The other point worth flagging: "receipt threshold" here is a single figure (34 USD) tied to this specific grade/band/stay row, not a company-wide constant — it's easy to assume it's a flat policy number that's the same everywhere, but it's actually indexed the same three ways (grade, band, stay) as the lodging and meal caps, so it changes with each combination.

Mapping "team manager" to G2 and "Singapore" to B2 was unambiguous — both legends had exact matches, no nearest-entry judgment call needed. Same for "four nights" → S2 (exact match).
