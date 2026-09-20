1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body

2. **Answer**
Multiplier: 2.88x. Minutes are rounded to the nearest 15 minutes.

3. **Source**
/v1/nodes/hard-moved-overtime/body
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body

4. **Notes**
The obvious first stop, payroll, is a trap: it still has an overtime table (`payslip-overtime`) but a warning page (`hard-moved-overtime`) says overtime premiums moved to attendance on 2026-01-01 and the payroll page is only correct for dates before that. Today is 2026-09-20, so payroll had to be abandoned in favor of attendance.

Inside attendance there is a second trap of the same shape: three versions of the overtime table exist (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and the oldest version says nothing about having been superseded — reaching for it or grabbing the "newest looking" table by name alone would silently give a stale answer. The legend-revision page was the only thing that made the date-gating explicit.

The biggest surprise was the "day" axis: I expected D1–D4 to be weekday/weekend/holiday-type categories, but the legend maps "two in the morning" directly to day code D4 — the axis is actually time-of-day, not calendar-day-type, despite being called "day". Had I assumed D-codes meant day-of-week and gone looking for what day of the week corresponds to "two in the morning," I'd have stalled or guessed wrong. Reading the legend literally rather than inferring from the row/column naming was what avoided that.

The other two qualifiers (hours="six hours"→H3, place="at my desk"→P1) mapped cleanly and unambiguously off their legends, no rounding/nearest-match judgment needed.
