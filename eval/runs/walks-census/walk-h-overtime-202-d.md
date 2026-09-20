1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body

2. **Answer**: Multiplier is 2.22x; minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body

4. **Notes**: The walk was straightforward since the question already gave the coded values (D3, H1, P3) rather than plain-language conditions, so no detour through the day/hours/place legend documents was needed — the row address could be assembled directly from the pattern shown in the `/v1/nodes/sec-hard-overtime` table listing. The one thing worth flagging: this table is explicitly marked as the current version in force from 2026-01-01, superseding `hard-overtime-v2` (2024-07-01 to 2025-12-31) and an older `overtime-rate-table`. Since today's date is 2026-09-20, the current table is the correct one to use, but it would be easy to grab a stale answer from one of the two superseded versions if not careful to check the "in force" dates.
