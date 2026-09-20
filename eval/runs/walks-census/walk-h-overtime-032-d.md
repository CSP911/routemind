1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body

2. **Answer**: Multiplier is 1.62x; minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p3/body

4. **Notes**: The row address for D1/H4/P3 was spelled out verbatim in the `sec-hard-overtime` table listing, so no legend lookup (day/hours/place definitions) was needed — the question already gave the codes directly. The one thing worth flagging: `sec-hard-overtime` is explicitly the *current* table (in force from 2026-01-01, replacing `hard-overtime-v2` and `overtime-rate-table`), and today's date is 2026-09-20, so this is the correct version. Easy to accidentally pull a superseded row if not careful about which table you opened.
