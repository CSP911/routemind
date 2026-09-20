1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body

2. **Answer**: Multiplier 1.41x; minutes rounded to the nearest 10 minutes. (In force from 2026-01-01, current version.)

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body

4. **Notes**: Straightforward walk — the row address for day D1/hours H2/place P4 was printed verbatim in the /v1/nodes/sec-hard-overtime table listing, so no legend lookup (day/hours/place codes) was needed since the question already gave codes directly. Only mild caution: the attendance area table listed both a current overtime table (`sec-hard-overtime`, in force from 2026-01-01) and two superseded versions (`hard-overtime-v2`, `overtime-rate-table`) plus a legend-revision doc; picked the current one per the question's implicit "what applies now" framing and per today's date (2026-09-20) falling within its effective range. Did not need to open the superseded versions or the legend files.
