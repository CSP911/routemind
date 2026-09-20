1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body

2. **Answer**
Multiplier: 1.80x. Minutes are rounded to the nearest 10 minutes.

3. **Source**
/v1/nodes/hard-overtime-legend-revision/body (confirmed which version applies)
/v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
/v1/nodes/hard-overtime-legend-hours/body (three hours → hours H2)
/v1/nodes/hard-overtime-legend-place/body (at my desk → place P1)
/v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p1/body (the answer)

4. **Notes**
The payroll region's own overtime page (/v1/nodes/hard-moved-overtime/body, not read in full — its warning was visible from the payroll table listing) is a trap: it flags that overtime premiums moved to attendance on 2026-01-01, so the real answer isn't in payroll at all. Easy to miss and start reading stale payroll figures.

Within attendance, there are three versions of the overtime table (pre-2024-07-01, 2024-07-01–2025-12-31 as `hard-overtime-v2`, and current `sec-hard-overtime` from 2026-01-01). The legend-revision page is explicit that reaching for the newest is wrong for dates before 2026-01-01 — since today is 2026-09-20, the current table was correct here, but this is clearly the kind of question where picking the wrong version silently gives a plausible-looking wrong multiplier. Worth double-checking the in-force date on every visit rather than assuming "current" is always right.

The three qualifiers (day/hours/place) each have their own legend, and none of the row addresses can be guessed — they had to be read off the table listing after resolving all three codes. "Three hours" mapped exactly to "hours H2" in the legend, no rounding/nearest-match judgment needed there, but the legend's own fallback rule ("take the nearest entry above it") suggests this table expects inexact inputs sometimes — worth flagging in case the values here were meant to test that path and I got lucky with an exact match.
