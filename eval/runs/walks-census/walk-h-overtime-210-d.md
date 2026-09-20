1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body

2. **Answer**: Multiplier is 2.28x. Minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body (confirmed which version applies for today's date, 2026-09-20)
/v1/nodes/hard-overtime-row-day-d3-hours-h2-place-p1/body (the answer)

4. **Notes**: The overtime subject has three superseded versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`) covering different date ranges, and the legend-revision page warns that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-20) falls in the current table's range, so `sec-hard-overtime` was correct, but it would have been easy to skip that check and just grab whichever row matched the qualifiers without verifying the date applied. The row itself was listed by exact address in the table listing (day-d3-hours-h2-place-p1), so no legend lookups for day/hours/place codes were needed — the question already gave the codes directly.
