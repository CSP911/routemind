1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body

2. **Answer**: Multiplier 2.10x; minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body

4. **Notes**: The walk was straightforward — the attendance region table names the current overtime table explicitly ("THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01"), and opening `sec-hard-overtime` lists all 64 day/hours/place rows individually, so the D2/H4/P3 combination could be picked by exact match without needing the day/hours/place legends. The one thing worth flagging: `sec-hard-overtime`'s description warns there are two superseded predecessor tables (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an older `overtime-rate-table`), reached via a `hard-overtime-legend-revision` warning file. Since today is 2026-09-20, the 2026-01-01-forward table is the right one, and the row itself restates that in-force date, so there was no real ambiguity — but it would have been easy to grab a superseded row if the date check were skipped.
