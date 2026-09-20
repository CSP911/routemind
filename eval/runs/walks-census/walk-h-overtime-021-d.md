1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body

2. **Answer**: Multiplier is 1.47x; minutes are rounded to the nearest 15 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p2/body

4. **Notes**: Nearly split effort by checking both /v1/regions/attendance and /v1/regions/payroll, since "multiplier" sounds like a pay concept — but payroll's own table explicitly warns overtime premiums moved to attendance on 2026-01-01, so payroll was a dead end. The attendance area lists both a current table (`sec-hard-overtime`, in force from 2026-01-01) and older superseded versions (`hard-overtime-v2`, and one before that referenced via `hard-overtime-legend-revision`) — since today is 2026-09-20, the current table was the correct pick, and the row address matched the day/hours/place codes in the question exactly, so no legend lookup was needed to translate a person's words into codes.
