1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body

2. **Answer**: Multiplier is 2.31x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body (found via /v1/regions/attendance → /v1/nodes/sec-hard-overtime)

4. **Notes**: The attendance region listed both a current and two superseded overtime tables (`sec-hard-overtime` current since 2026-01-01, `hard-overtime-v2` superseded 2024-07-01 to 2025-12-31, and an older `overtime-rate-table`), plus a "legend-revision" warning file calling out the versioning. Easy to grab a stale row here — I made sure to open `sec-hard-overtime` (explicitly marked "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01") rather than `hard-overtime-v2`, and today's date (2026-09-20) falls within its validity window. The question gave the day/hours/place codes directly (D3/H2/P2), so I didn't need to consult the day/hours/place legend files to translate a plain-language scenario into codes — but those legends exist and would be necessary if the codes weren't already given.
