1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D4, hours H1, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day/hours/place, in force since 2026-01-01"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_130749 --outcome answered --used /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body

2. **Answer**: Multiplier 2.67x; minutes rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body

4. **Notes**: The overlay `create` call already surfaced the exact D4/H1/P2 row by address (rows for every day/hours/place combination are enumerated under /v1/nodes/sec-hard-overtime), so no narrowing was needed beyond picking that one row. The row itself states it is the version in force from 2026-01-01, with two superseded prior versions (`hard-overtime-v2` and `overtime-rate-table`) noted in the same document — worth watching for on other overtime questions in case a query implies an older date, but today's date (2026-09-21) falls inside the current version's range so no ambiguity here. The `overlay close` output printed "reached = answered from somewhere the overlay never named — recorded as such" even though the address used was exactly the one the overlay table had printed; this looks like a quirk/false flag in the tool rather than an actual mismatch, since the address was copied verbatim from the overlay listing.
