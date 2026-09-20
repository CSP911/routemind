1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body (skipped — table listing already showed the move; not actually read)
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body

2. **Answer**: Multiplier 1.23x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body (confirmed which version is in force for today's date)
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body (the figures)

4. **Notes**: Payroll's own table listing already warned that overtime premiums moved to attendance on 2026-01-01, so I never had to open the old payroll body page — just enough to see the warning and redirect. The real trap was in attendance itself: there are three superseded versions of the overtime rate (pre-2024-07-01, 2024-07-01–2025-12-31 as `hard-overtime-v2`, and current `sec-hard-overtime` from 2026-01-01). Since today is 2026-09-20, the current table is correct, but the legend-revision page explicitly warns that grabbing "the newest" is only safe here because the date happens to fall after 2026-01-01 — for a 2025-dated question the middle version would be the right one, not the current or oldest. Once inside `sec-hard-overtime`, the D1/H1/P2 combination had its own exact row already listed, so no legend lookups for day/hours/place codes were needed — it resolved directly without ambiguity.
