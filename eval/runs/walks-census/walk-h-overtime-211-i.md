1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body

2. **Answer**: Multiplier 2.31x; minutes rounded to the nearest 10 minutes. (Approval was needed in advance, and the hours count toward the monthly cap.)

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body

4. **Notes**: The payroll area's overtime page is a trap — it explicitly warns that overtime, night and holiday premium rates moved to attendance on 2026-01-01, so the payroll table itself is stale for a 2026-09-20 question. Attendance in turn has two overtime tables (a superseded `hard-overtime-v2` for 2024-07-01–2025-12-31 and the current `sec-hard-overtime` in force from 2026-01-01); today's date puts the query on the current one, but it would have been easy to grab the older version by mistake since both are listed side by side. The row table itself is indexed by opaque D/H/P codes with no plain-language hints, so each of "Liberation day", "three hours", and "out at a client's office" had to be resolved separately through the three legend files before the address for the actual row (D3-H2-P2) could be constructed — nothing about the row address is guessable without reading all three legends first.
