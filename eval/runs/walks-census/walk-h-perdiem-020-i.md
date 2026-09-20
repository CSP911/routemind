## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

## Answer
For a junior analyst (grade G1) traveling to Jakarta (band B3) for one night (stay S1), under the overseas per-diem table in force from 2026-01-01 (current as of today, 2026-09-20):

- Lodging cap: **127 USD per night**
- Receipt required above: **36 USD** (the receipt threshold for this row)

(For context, also in this row: meals 66 USD/day, incidentals 13 USD/day — not asked for but part of the same row.)

## Source
- /v1/regions/expense (navigation)
- /v1/nodes/sec-hard-perdiem (navigation to the current per-diem table)
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → G1)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → B3)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → S1)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s1/body (the figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms current table applies to today's date)

## Notes
- The expense area table explicitly warns that overseas per-diem has three versions in force over different date ranges, and that the oldest version says nothing about having been superseded — it would be easy to grab `overseas-rates` or `hard-perdiem-v2` without noticing they're outdated. I checked the revision legend explicitly to confirm 2026-09-20 falls under the current table (`sec-hard-perdiem`, from 2026-01-01 onward) before trusting the figures.
- The per-diem table is indexed by three separate codes (grade, band, stay) that must each be resolved via a separate legend file before the row address can be built — nothing warns you up front that all three are needed, so it would be easy to guess a row address instead of reading the legends. The instructions insist addresses are never to be constructed, only used as printed, so reading all three legends first was necessary, not optional.
- "Receipt threshold" appears directly inside the specific per-diem row (not in the general `evidence` table), which is a slightly odd place to look for it — I initially expected the receipt/evidence rule to live in `/v1/nodes/evidence`, but the grade/band/stay-specific threshold shown here (36 USD) is the one that actually answers the question, since it varies by row rather than being a flat company-wide number.
