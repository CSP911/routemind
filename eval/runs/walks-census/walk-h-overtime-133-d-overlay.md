1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D2, hours H4, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_fe769b --outcome answered --used /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body

2. **Answer**: Multiplier is 2.13x. Minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body

4. **Notes**: The overlay create step listed the whole /v1/nodes/sec-hard-overtime table (67 rows, one per day/hours/place combination) rather than the single row needed, since I could only name the table as a member up front. The exact row address for D2/H4/P4 was visible directly in that listing (`hard-overtime-row-day-d2-hours-h4-place-p4`), so I read it straight away without needing the legend files (hard-overtime-legend-day/hours/place) since the question already gave the qualifiers D2/H4/P4 pre-resolved rather than raw dates/hours/locations to classify. One thing worth flagging: the overlay close output said "reached = answered from somewhere the overlay never named" — this is because I read the specific row's address directly rather than first doing an explicit `overlay add` for it; the row was still reachable through the table member I'd already added, so this is a bookkeeping note, not an error. Also worth noting: the legend files and the superseded versions (hard-overtime-v2, overtime-rate-table) are still listed in the region and could easily be mistaken for the current figures if not for the "in force from 2026-01-01" note confirming this is the current table.
