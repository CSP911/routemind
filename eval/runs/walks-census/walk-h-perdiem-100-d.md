## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body

## Answer
Lodging (hotel), per night: 159 USD. Receipt threshold: 22 USD — spend above this amount requires a receipt to be kept.
(This is the current overseas per-diem table, in force from 2026-01-01.)

## Source
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s1/body

## Notes
The question gave grade/band/stay codes directly (G2, B1, S1), so no detour through the
grade/band/stay legends was needed — the row address could be built straight from the table
listing at /v1/nodes/sec-hard-perdiem.

The one place this could have gone wrong: the expense area table lists three per-diem-related
documents — `hard-perdiem-legend-revision`, `hard-perdiem-v2` (superseded, 2024-07-01 to
2025-12-31), and `sec-hard-perdiem` (current, from 2026-01-01). It would be easy to grab the v2
document by mistake since it sorts near the top of the listing and looks equally authoritative at
a glance. The revision-legend file and the table's own description both flag `sec-hard-perdiem`
as the one in force today (2026-09-20), which is what was used.
