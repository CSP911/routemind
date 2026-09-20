1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body

2. **Answer**: Multiplier 1.20x; minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body

4. **Notes**: The question's "D1, H1, P1" turned out to be literal codes used by the current overtime table (`sec-hard-overtime`), not placeholders to resolve via a legend — the table is indexed by exactly those day/hours/place codes (D1–D4, H1–H4, P1–P4), so the row address could be built directly from the question's own terms. Easy to go wrong here: payroll's own table still lists an overtime page (`hard-moved-overtime`), but it's a warning that the rates moved to attendance on 2026-01-01, so following it would have led to a stale/redirect page rather than the answer. Also present in attendance were `hard-overtime-v2` (superseded, 2024-07-01 to 2025-12-31) and `hard-overtime-legend-revision` — worth noting because there are three historical versions of this rate, and grabbing the wrong one silently gives a plausible but outdated multiplier. Confirmed `sec-hard-overtime` is the one in force from 2026-01-01, which matches today's date (2026-09-20), before reading the row.
