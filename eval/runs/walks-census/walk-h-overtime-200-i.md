1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body

2. **Answer**
Multiplier: 2.16x. Rounding: to the nearest 5 minutes.

3. **Source**
- /v1/nodes/hard-overtime-legend-day/body (Liberation Day → day D3)
- /v1/nodes/hard-overtime-legend-hours/body (about ninety minutes → hours H1)
- /v1/nodes/hard-overtime-legend-place/body (at my desk → place P1)
- /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p1/body (multiplier and rounding)
- /v1/nodes/hard-overtime-legend-revision/body (confirms current table applies for 2026-09-20)

4. **Notes**
The attendance area lists three overtime tables: the current one (`sec-hard-overtime`, in force since 2026-01-01), a superseded `hard-overtime-v2` (2024-07-01 to 2025-12-31), and an even older `overtime-rate-table`. It would be easy to grab the wrong version if the question were dated earlier — the revision legend explicitly warns that "reaching for the newest is wrong for anything before 2026-01-01." Today's date (2026-09-20) is safely inside the current table's range, so `sec-hard-overtime` was correct, but this is the kind of question where the date has to be checked, not assumed. The three qualifiers (day, hours, place) each needed their own legend lookup since the row addresses use opaque codes (D3/H1/P1) not the plain-language terms from the question — skipping any one of the three legends would have made it impossible to build the correct row address.
