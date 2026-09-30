1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Saturday, six hours, at desk: what multiplier applies, and to what rounding are minutes taken?" --member /v1/regions/payroll "overtime pay multiplier likely defined in payroll" --member /v1/regions/attendance "Saturday/weekend work and time rounding rules likely under attendance"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_6a8936 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body

2. **Answer**: Multiplier is 1.92x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body

4. **Notes**: The overtime rate subject has three versions in force over different date ranges, and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20/21) falls after that cutoff, so the current table `sec-hard-overtime` applies — but this was a real branch point where picking the wrong version silently gives a plausible but wrong multiplier. The row itself is indexed by three separate qualifier legends (day, hours, place) that must each be translated from plain English before the row address can be assembled: "a Saturday" → D2, "six hours" → H3 (an exact match, not a nearest-band guess), "at my desk" → P1 (also exact). Easy to trip up by trying to guess the row address directly instead of resolving all three legends first — the tool is explicit that addresses must never be constructed, only read off a table.
