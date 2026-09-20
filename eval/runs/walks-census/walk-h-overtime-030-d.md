1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body

2. **Answer**: Multiplier is 1.56x. Minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body (confirmed current/in-force via /v1/nodes/hard-overtime-legend-revision/body)

4. **Notes**: The payroll region's top-level table explicitly warns that overtime premiums moved to attendance on 2026-01-01, so starting in payroll was a natural but wrong first guess — the real data lives under attendance. Once there, attendance lists three overtime-rate versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onwards) with an explicit warning that "the oldest says nothing at all about having been replaced," meaning a naive first hit could silently be the wrong vintage. Today's date (2026-09-20) falls in the current table's range, so `/v1/nodes/sec-hard-overtime` was correct, and it turned out to index the D1/H4/P1 row directly by name rather than requiring cross-referencing separate day/hours/place legend tables — no ambiguity in matching the qualifiers to codes was needed here since the address itself spelled out d1/h4/p1.
