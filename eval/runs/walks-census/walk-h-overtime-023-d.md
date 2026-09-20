1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body

2. **Answer**: Multiplier is 1.53x. Minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p4/body

4. **Notes**: The walk was straightforward — the row addresses spell out the day/hours/place codes directly (`hard-overtime-row-day-d1-hours-h3-place-p4`), so once `/v1/nodes/sec-hard-overtime` was open, the right row was obvious without needing the legend files. The one thing worth flagging: this table has three historical versions (`hard-overtime-v2` for 2024-07-01–2025-12-31, and an older `overtime-rate-table`), all cross-linked from the same area. I confirmed `sec-hard-overtime` is explicitly marked "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01" and today's date (2026-09-20) falls inside that range, so this is the correct version — but it would be easy to grab a superseded row by mistake if you didn't check the effective dates.
