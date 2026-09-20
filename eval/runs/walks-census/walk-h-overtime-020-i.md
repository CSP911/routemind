1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body

2. **Answer**
Multiplier: 1.44x. Rounding: to the nearest 15 minutes.

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p1/body

4. **Notes**
The payroll region's table listing warned up front that overtime premium rates moved to attendance on 2026-01-01 and that the payroll page is now the old rule — that steered me away from payroll before I wasted a read on it. Inside attendance, there are explicitly THREE historical versions of the overtime rate (a legend-revision warning file, `hard-overtime-v2` for 2024-07-01 to 2025-12-31, and the current `sec-hard-overtime` for 2026-01-01 onward); with today's date being 2026-09-20, `sec-hard-overtime` is unambiguously current, but it would be easy to grab the superseded v2 node by pattern-matching on the word "overtime" alone without checking the effective-date warning first. The row table itself is a 64-row cross product (4 day codes x 4 hour codes x 4 place codes) with no shortcut — the three legends must each be read separately to translate "ordinary Tuesday" / "six hours" / "at my desk" into D1/H3/P1 before the single matching row address can be built from the pattern the table already printed (not invented). Each legend also carries a "nearest entry above it" fallback instruction, which wasn't needed here since all three inputs matched an entry exactly, but is worth flagging as a source of ambiguity in less clean-cut phrasings of the same question.
