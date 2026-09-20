1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body

2. **Answer**: Multiplier 2.94x; minutes rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p3/body

4. **Notes**: The attendance area lists both a current overtime table (`sec-hard-overtime`, in force from 2026-01-01) and two superseded ones (`hard-overtime-v2`, `overtime-rate-table`) reachable from the same region — easy to grab the wrong vintage if you don't check the "in force from" date against today (2026-09-20) and confirm via the row body's footer, which I did. The three legends map plain-language inputs to codes exactly, with no fuzzy matching needed here: "two in the morning" → D4, "six hours" → H3, "on standby at home" → P3, all literal entries in their respective legend tables rather than nearest-match approximations. The legend day table's literal listing of "two in the morning" as its own day-type code (D4) rather than a time-of-day modifier on an ordinary day was the one place I paused — it reads unusually, as if day type folds in a "graveyard shift" condition rather than just calendar day, but the table is explicit and left no ambiguity once read.
