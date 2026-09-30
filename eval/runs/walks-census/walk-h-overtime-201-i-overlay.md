1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Liberation day, about ninety minutes, out at a client's office: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/holiday work rules likely live here" --member /v1/regions/payroll "overtime multiplier and rounding could be a payroll computation rule"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8a52bb --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body
```

2. **Answer**
Multiplier: 2.19x. Rounding: to the nearest 5 minutes.

3. **Source**
- /v1/nodes/hard-overtime-legend-revision/body (established that today, 2026-09-21, falls under the current table, not the two older versions)
- /v1/nodes/hard-overtime-legend-day/body (Liberation Day → day D3)
- /v1/nodes/hard-overtime-legend-hours/body (about ninety minutes → hours H1)
- /v1/nodes/hard-overtime-legend-place/body (out at a client's office → place P2)
- /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body (the row itself: multiplier and rounding)

4. **Notes**
Overtime rate is versioned three times (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), each with different in-force dates and a different number of qualifiers, and the oldest version gives no hint that it's been superseded. I checked the legend-revision doc before trusting the current table, since today's date (2026-09-21) needed confirming against the 2026-01-01 cutover rather than assumed. The three phrases in the question map onto separate legend tables (day/hours/place), each keyed by wording rather than by any obvious code, so all three had to be read before the row address could be built — none of it is guessable from the question text alone. "About ninety minutes" was an exact, unambiguous match to the H1 legend entry, so no nearest-value judgment call was needed there.
