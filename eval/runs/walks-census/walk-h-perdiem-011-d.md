## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s2/body

## Answer
Lodging cap: 115 USD per night. Receipt threshold: 30 USD — you must keep the receipt for any spend above that amount.

## Source
/v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s2/body

## Notes
The expense region's table listed three superseded/overlapping per-diem documents (`hard-perdiem-legend-revision`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`) — easy to grab the wrong version by mistake. The warning text flagged `hard-perdiem-v2` as covering 2024-07-01 to 2025-12-31 (superseded) and `sec-hard-perdiem` as the current table from 2026-01-01, which matches today's date (2026-09-20), so `sec-hard-perdiem` was the correct one to open. Once inside, the row address for grade G1/band B2/stay S2 was printed literally (`hard-perdiem-row-grade-g1-band-b2-stay-s2`), so no guessing was needed — the question's grade/band/stay codes mapped directly onto the table's naming scheme.
