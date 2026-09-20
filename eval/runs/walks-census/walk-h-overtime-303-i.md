1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4/body

2. **Answer**: Multiplier 2.73x; minutes rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day
/v1/nodes/hard-overtime-legend-hours
/v1/nodes/hard-overtime-legend-place
/v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4

4. **Notes**: The payroll area's own overtime page (/v1/nodes/hard-moved-overtime) is a dead end by design — it just redirects to attendance as of 2026-01-01, so that stop was necessary but yielded nothing itself. The real trap is the day-type legend: "two in the morning" is listed there as a *day code* (D4), not a time-of-day modifier on an ordinary weekday row. It would be easy to read "2am" as merely qualifying which hours/rate band applies and go looking for a night-shift multiplier on a D1 (ordinary Tuesday) row instead — but the legend explicitly maps "two in the morning" itself to D4, overriding whatever the calendar day would otherwise be. The hours ("about ninety minutes" → H1) and place ("from home" → P4) legends matched the question's wording exactly, so no nearest-entry judgment call was needed there. I did not use the "nearest entry above it" fallback rule at all since all three inputs had literal matches in their respective legends.
