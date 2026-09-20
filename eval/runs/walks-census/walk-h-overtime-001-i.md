1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body

2. **Answer**: Multiplier is 1.23x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body

4. **Notes**: Overtime rate has three superseded versions indexed by different numbers of qualifiers (1, 2, then 3), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-20) falls under the current table `sec-hard-overtime`, so no correction was needed here, but this is exactly the kind of question where grabbing the current table without checking the revision page first would silently give the wrong answer for an older date. The three qualifiers ("ordinary Tuesday" → D1, "about ninety minutes" → H1, "out at a client's office" → P2) are each spelled out verbatim in their respective legends, which made the mapping unambiguous — no nearest-entry guessing was required.
