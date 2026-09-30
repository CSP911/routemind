1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "For day D3, hours H2, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "old overtime page, warns it moved to attendance 2026-01-01" --member /v1/regions/attendance "current home of overtime/night/holiday premium rates"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_5f81d3 --outcome answered --used /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body

2. **Answer**: Multiplier 2.31x; minutes rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p2/body

4. **Notes**: The payroll region's own table still lists overtime-looking pages, but its top-level description flags a WARNING that overtime/night/holiday premium rates moved to attendance on 2026-01-01 — the payroll page (`hard-moved-overtime`) is the old, superseded rule. Went to attendance instead, where `sec-hard-overtime` is explicitly labeled "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01." That table is indexed directly by day/hours/place codes, so the row for D3/H2/P2 existed verbatim as `hard-overtime-row-day-d3-hours-h2-place-p2` — no need to consult the day/hours/place legends since the question already gave codes, not descriptions. Also noted there are three historical versions of this table (`hard-overtime-legend-revision`, `hard-overtime-v2`, `overtime-rate-table`), but today (2026-09-21) falls under the current version's effective date, so no version conflict applied. The overlay close command timed out client-side and was moved to a background task, but the answer itself was already fully confirmed from the read before that happened.
