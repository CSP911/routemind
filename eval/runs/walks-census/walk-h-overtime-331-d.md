1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body

2. **Answer**:
Multiplier: 3.03x
Rounding: to the nearest 20 minutes

3. **Source**:
/v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body

4. **Notes**:
The attendance area listed both a current overtime table (`sec-hard-overtime`, in force from 2026-01-01) and two older superseded ones (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an even older `overtime-rate-table`). Since today's date is 2026-09-20, the current table applies, and it was easy to pick the right one because the table's own description flags the older pages as "superseded." The D4/H4/P2 row address was printed directly by the table listing, so no guessing or construction of addresses was needed — a straight three-hop walk from region to table to row.
