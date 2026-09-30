1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "For day D2, hours H2, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-legend-revision/body "warning about three versions of overtime rate with different dates, need to confirm which applies today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_091663 --outcome answered --used /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body /v1/nodes/hard-overtime-legend-revision/body

2. **Answer**: Multiplier 1.80x; minutes are rounded to the nearest 10 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body
- /v1/nodes/hard-overtime-legend-revision/body

4. **Notes**: The attendance region lists three overtime-rate pages with overlapping subject matter — the current table (`sec-hard-overtime`, in force from 2026-01-01, indexed by three qualifiers: day/hours/place), a superseded second version (`hard-overtime-v2`, 2024-07-01 to 2025-12-31, indexed by only two qualifiers), and an oldest version (`overtime-rate-table`, indexed by one qualifier) that per the revision legend "says nothing at all about having been replaced." Payroll also has a page that used to hold overtime premiums but explicitly warns it moved to attendance on 2026-01-01 — a plausible wrong turn if searched from payroll first. Today's date (2026-09-21) falls in the current table's window, so `sec-hard-overtime`'s D2/H2/P1 row was the right one to read, but the legend-revision page was worth checking explicitly since the three versions use different indexing schemes (one/two/three qualifiers) and a casual reader could easily grab the wrong version's row for a differently-dated question. The overlay close reported the specific row as "reached" rather than "member" — it was surfaced as a child row when `sec-hard-overtime` was added, not added individually — but this didn't affect the answer.
