## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body
./bench/rmcli.py table /v1/nodes/evidence

## Answer
Lodging cap: 135 USD per night. Receipt required for any spend above 42 USD (the receipt threshold for this row).
(For reference, same row also gives meals 76 USD/day and incidentals 15 USD/day, though not asked.)

## Source
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s3/body

## Notes
- The expense area warns up front that overseas per-diem has three versions in force over different date ranges, and that the oldest version says nothing about being superseded — reaching for the newest table without checking the date would be wrong for a question dated before 2026-01-01. Today (2026-09-20) falls in the current version's range (`sec-hard-perdiem`, from 2026-01-01), so that was the correct table, but this was the one place I could easily have gotten a stale answer without noticing.
- "Eight nights" maps exactly to stay code S3 in the legend (one night/S1, four nights/S2, eight nights/S3, three weeks/S4) — no rounding or nearest-match judgment call was needed here, unlike the legend's fallback instruction for unlisted values.
- The per-diem row itself carries its own "Receipt threshold" field (42 USD) alongside the lodging cap, distinct from the general evidence/qualifying-evidence tables under `/v1/nodes/evidence`. I did not descend into the general evidence table's receipt rules, since the per-diem row already gives a threshold specific to this grade/band/stay combination and mixing the two could have produced a contradictory or irrelevant figure — worth flagging in case the two are meant to interact and I missed it.
