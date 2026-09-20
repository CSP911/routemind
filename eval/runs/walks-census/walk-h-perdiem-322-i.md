## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body

## Answer
Lodging (hotel) cap: 327 USD per night. Receipt threshold: 54 USD — spend above that amount requires a receipt to be kept as evidence.
(For context, the same row also gives meals at 103 USD/day and incidentals at 21 USD/day, but those weren't asked for.)

## Source
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s3/body (final figures)

## Notes
The expense area's own table entry warned upfront that overseas per-diem has three superseded versions layered on top of each other (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, `overseas-rates`) — easy to grab a stale table if you don't stop to check dates. I went straight for `sec-hard-perdiem`, which is explicitly labeled current since 2026-01-01, and today's date (2026-09-20) falls inside that window, so no need to open the revision-legend or v2 doc. The row itself also restates "in force from 2026-01-01" as a footer, which is a nice cross-check but did mean I nearly opened one more file to double-confirm before deciding it was redundant.

The three legends (grade/band/stay) are the only place the plain-English inputs map to row codes — the row files don't repeat the mapping, so skipping any one of the three legends would have made it impossible to build the address `hard-perdiem-row-grade-g4-band-b3-stay-s3` correctly. "Eight nights" maps exactly to stay S3 with no rounding ambiguity, which was reassuring since the legend's fallback rule ("take the nearest entry above it") suggested I might have to make a judgment call — I didn't need to here.
