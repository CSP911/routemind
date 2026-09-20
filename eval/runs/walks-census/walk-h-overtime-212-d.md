1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body

2. **Answer**: Multiplier is 2.34x; minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p3/body

4. **Notes**: The row address for D3/H2/P3 was printed verbatim in the `sec-hard-overtime` table listing, so no construction was needed. The main thing to watch was picking the *current* overtime table — `attendance` region lists both `sec-hard-overtime` (current, in force from 2026-01-01) and a superseded `hard-overtime-v2` (2024-07-01 to 2025-12-31), plus a `hard-overtime-legend-revision` warning file. Today's date (2026-09-20) falls under the current table, so `sec-hard-overtime` was correct; it would have been easy to grab the superseded v2 row by mistake if the dates weren't checked.
