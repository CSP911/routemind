1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body

2. **Answer**: Multiplier 1.38x. Rounding: to the nearest 10 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (mapped "an ordinary Tuesday" → day D1)
- /v1/nodes/hard-overtime-legend-hours/body (mapped "three hours" → hours H2)
- /v1/nodes/hard-overtime-legend-place/body (mapped "on standby at home" → place P3)
- /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p3/body (the actual figures: 1.38x, nearest 10 minutes)

4. **Notes**: The initial detour into /v1/regions/payroll was necessary but nearly a dead end — payroll's own overtime page (`hard-moved-overtime`) is explicitly superseded and just points to attendance, so it would have been wrong to read the multiplier from anywhere in payroll. The overtime table in attendance also carries two older superseded versions (`hard-overtime-v2`, `overtime-rate-table`) sitting right next to the current one (`sec-hard-overtime`) — easy to grab the wrong vintage if you don't check the "in force from 2026-01-01" note. The three legends had to be read literally and separately (day, hours band, place) since the row addresses are built from codes, not from plain-language terms — nothing in the question's wording ("ordinary tuesday", "three hours", "standby at home") appears verbatim in the row list, only in the legends. All three inputs matched an exact legend row, so no "nearest entry" fallback was needed.
