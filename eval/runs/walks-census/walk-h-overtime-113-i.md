1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body

2. **Answer**: Multiplier 1.89x; minutes rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body

4. **Notes**: The three legends (day, hours, place) had to be read first to translate "a Saturday" → D2, "three hours" → H2, "from home" → P4 before the correct row address could be composed — the row addresses are not discoverable by guessing, they're built from the legend codes. The near-miss risk was the day legend: it lists both date-based codes (Tuesday, Saturday, holiday) and a time-of-day code ("two in the morning" → D4), which could tempt picking D4 if the question were read as being about timing rather than the day of week — but "a Saturday" maps cleanly to D2 with no ambiguity. Also had to confirm the row came from the current table (`sec-hard-overtime`, in force since 2026-01-01) rather than the superseded `hard-overtime-v2` — today's date (2026-09-20) falls under the current version, so no ambiguity there either.
