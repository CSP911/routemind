1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body

2. **Answer**: Multiplier is 2.49x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (mapped "Liberation Day" → day D3)
- /v1/nodes/hard-overtime-legend-hours/body (mapped "six hours" → hours H3)
- /v1/nodes/hard-overtime-legend-place/body (mapped "from home" → place P4)
- /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body (the answer: 2.49x, rounding to nearest 15 minutes)

4. **Notes**: The overtime table (/v1/nodes/sec-hard-overtime) has 64 rows named only by codes (D1-D4, H1-H4, P1-P4); the codes are meaningless without the three legend files, which had to be fetched separately before the right row address could be assembled. It would have been easy to jump straight to a guessed row address, but the instructions say never to build an address — each legend confirmed the exact code needed. Also worth flagging: there is a superseded row-naming/versioning history (`hard-overtime-v2`, `overtime-rate-table`) noted in the current row's footer; since today (2026-09-20) falls after the current table's 2026-01-01 start date, the current table (`sec-hard-overtime`) was the correct one to use, not the superseded versions — but this was easy to get wrong if the "legend-revision" warning file had been skipped. Nothing else here was ambiguous: "Liberation Day" and "from home" mapped cleanly to single legend rows with no fuzzy nearest-match judgment needed.
