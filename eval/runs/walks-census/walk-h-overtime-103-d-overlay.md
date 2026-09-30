1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D2, hours H1, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01"
./bench/rmcli.py overlay remove --id ov_2026-09-20_2ea0b0 --address /v1/nodes/sec-hard-overtime --why "was the table container itself, not needed once the exact row is identified"
./bench/rmcli.py overlay add --id ov_2026-09-20_2ea0b0 --address /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body --why "the exact row for day D2, hours H1, place P4"
./bench/rmcli.py overlay add --id ov_2026-09-20_2ea0b0 --address /v1/nodes/hard-overtime-legend-hours/body --why "explains how overtime hours are banded and rounding rule context, read before choosing rounding"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2ea0b0 --outcome answered --used /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body

2. **Answer**: Multiplier 1.77x. Rounding: to the nearest 5 minutes. (Current table, in force from 2026-01-01.)

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body

4. **Notes**: Adding the table container `/v1/nodes/sec-hard-overtime` as the overlay's first member and then removing it wiped the overlay back to 0 rows instead of leaving the other rows in place — worth knowing that removing a "container" address seems to clear the whole set, not just that one row. No real ambiguity otherwise: the attendance area table explicitly named the current (post-2026-01-01) overtime table as `sec-hard-overtime`, opening it listed one row per exact (day, hours, place) triple, and `day-d2-hours-h1-place-p4` matched the question's qualifiers exactly, so there was no need to fall back to the legend documents to disambiguate day/hour/place codes. I pulled in the hours-legend as a safety check but never needed to read it since the row itself stated the rounding rule plainly.
