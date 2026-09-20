1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body

2. **Answer**
Multiplier: 2.40x. Rounding: to the nearest 15 minutes.

3. **Source**
/v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body

4. **Notes**
The payroll area is the natural first guess for "multiplier" language, but its own table front page carries an explicit warning that overtime/night/holiday premium rates moved to attendance on 2026-01-01 — the payroll page is superseded. That warning kept me from reading the stale `hard-moved-overtime` body as if it were current. Within attendance, there were two overtime tables listed: `hard-overtime-v2` (superseded, 2024-07-01 to 2025-12-31) and `sec-hard-overtime` (current, in force from 2026-01-01). Today's date (2026-09-20) falls under the current table, so `sec-hard-overtime` was the correct pick — easy to grab the wrong version if you don't check the effective dates. The row address itself was printed exactly by the table listing (`hard-overtime-row-day-d3-hours-h3-place-p1`), so no address construction was needed — just matching D3/H3/P1 against the row list.
