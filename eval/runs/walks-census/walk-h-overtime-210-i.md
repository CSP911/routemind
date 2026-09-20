1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body
```

2. **Answer**
Multiplier: 2.28x. Rounding: to the nearest 10 minutes.
(Also noted on this row: approval needed in advance — yes; counts toward the monthly cap — yes.)

3. **Source**
- /v1/nodes/hard-overtime-legend-day/body (Liberation Day → day D3)
- /v1/nodes/hard-overtime-legend-hours/body (three hours → hours H2)
- /v1/nodes/hard-overtime-legend-place/body (at my desk → place P1)
- /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body (multiplier and rounding)

4. **Notes**
The current overtime rate table (`/v1/nodes/sec-hard-overtime`) is in force from 2026-01-01, and today is 2026-09-20, so it applies without needing to check the superseded `hard-overtime-v2` or `overtime-rate-table` versions — but the attendance table listing flags all three, and it would have been easy to grab a superseded row by accident if I hadn't checked the "in force" dates. The three qualifiers (day/hours/place) each have to be translated through a separate legend file rather than matched literally against the question's wording — "Liberation Day," "three hours," and "at my desk" all map directly and unambiguously to D3, H2, and P1 respectively, so no fuzzy nearest-entry judgment call was needed here, but the legend files explicitly warn that one may be required in other cases. The row address itself (`hard-overtime-row-day-d3-hours-h2-place-p1`) is not something to guess or construct by pattern — I only used it because the table listing printed it verbatim after resolving the three codes.
