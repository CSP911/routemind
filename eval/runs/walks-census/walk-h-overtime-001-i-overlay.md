1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Ordinary Tuesday, ~90 minutes at client's office: what multiplier applies, and to what rounding are minutes taken?" --member /v1/regions/attendance "overtime/time tracking rules likely live here" --member /v1/regions/payroll "overtime pay multiplier may be defined in payroll rules"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2c37c0 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body

2. **Answer**: Multiplier 1.23x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body

4. **Notes**: The payroll region member I added to the overlay turned out to be a dead end — a note there (`hard-moved-overtime`) says overtime premiums moved to attendance on 2026-01-01, so payroll wasn't where the answer lived even though "multiplier" sounds like a pay term. The real work was in the attendance region's `sec-hard-overtime` table, which is indexed by three codes (day/hours/place) via three separate legend files rather than by plain English — you have to translate "an ordinary Tuesday" → D1, "about ninety minutes" → H1, "out at a client's office" → P2 before the row address even exists, and each legend's wording matches the question's phrasing closely enough that it's easy to skip straight to guessing a row address instead of reading all three legends first. I also had to be careful about versioning: there are three historical revisions of this table (`overtime-rate-table`, `hard-overtime-v2`, and the current `sec-hard-overtime`), each with their own legend/row values, and a `hard-overtime-legend-revision` warning file flags this explicitly. Today (2026-09-20/21) falls under the current table, in force since 2026-01-01, so I used that one and did not need to check the superseded versions. The overlay's `close` reported these addresses as "reached" rather than "used" since I hadn't added the specific node addresses as overlay members — only the parent regions — which is a mechanical quirk of the tool, not an ambiguity in the answer itself.
