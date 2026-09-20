## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

## Answer
Lodging cap: 231 USD per night. Receipt required above 32 USD.

(Department head → grade G3; Tokyo → band B1; eight nights → stay S3.)

## Source
- /v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → B1)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → S3)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body (231 USD lodging, 32 USD receipt threshold)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms current table applies for a 2026-09-20 question)

## Notes
The expense area table lists three per-diem documents with overlapping subject lines: `hard-perdiem-legend-revision`, `hard-perdiem-v2` (superseded), and `sec-hard-perdiem` (current). It would be easy to grab `hard-perdiem-v2` by mistake since its label doesn't scream "outdated" until you read the body — the legend-revision doc is what actually pins today's date (2026-09-20) to the current table. I checked it last as a confirmation rather than first, which worked out here since the region table already flagged `sec-hard-perdiem` as "current table since 2026-01-01," but for a question with an ambiguous or past date, the revision doc should be read before picking a row, not after.

The three legends (grade, band, stay) are each their own lookup and have to be resolved before the row address can be built — none of it is guessable from the question text alone ("department head" isn't literally "G3" anywhere until you read the grade legend). Also note the row itself carries its own receipt threshold (32 USD) distinct from any general evidence-table threshold — I did not need to consult `/v1/nodes/evidence` since this row was self-contained and more specific.
