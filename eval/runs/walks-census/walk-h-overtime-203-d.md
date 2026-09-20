1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body

2. **Answer**: Multiplier is 2.25x. Minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body

4. **Notes**: The attendance region listing flagged that overtime rules have older superseded versions (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and `overtime-rate-table` before that) alongside a revision-legend warning file. It would have been easy to grab a superseded version by mistake if the table listing hadn't explicitly labeled `sec-hard-overtime` as "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01." Since today's date (2026-09-20) falls within that current table's validity window, this was the correct row. The table at `sec-hard-overtime` conveniently listed the exact row address for D3/H1/P4 directly (no need to cross-reference separate day/hours/place legends), so no ambiguity remained once the right table was identified.
