1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body

2. **Answer**: Multiplier is 2.49x; minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p4/body

4. **Notes**: The walk was straightforward — the region table's description for `/v1/regions/attendance` explicitly mentions "how much overtime, night and holiday hours pay, by day type, hours and place (current table since 2026-01-01)," which pointed directly at `sec-hard-overtime`, and that table's row list is indexed by exact day/hours/place codes, so `day-d3-hours-h3-place-p4` was an exact, unambiguous match with no need to consult the legends. The one thing worth flagging: this table's own listing warns it superseded two older versions (`hard-overtime-v2` for 2024-07-01–2025-12-31, and `overtime-rate-table` before that). Since today's date (2026-09-20) falls within the current version's effective range (from 2026-01-01), I used the current table and did not need the older ones — but a careless reader could easily grab a superseded row by address pattern alone without checking the effective-date note.
