1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body

2. **Answer**: Multiplier 2.52x; minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p1/body

4. **Notes**: The payroll area's own overtime page (`hard-moved-overtime`) warns that overtime premiums moved to attendance on 2026-01-01, which correctly redirected me away from payroll before I wasted a lookup there. Within attendance, there are two competing tables (a superseded `hard-overtime-v2` for 2024-07-01 to 2025-12-31, and the current `sec-hard-overtime` for 2026-01-01 onward) — today's date (2026-09-20) makes the current table the right one, but it would be easy to grab the wrong version if not careful. The three legends (day/hours/place) are not obvious from the question's wording alone: "Liberation day" had to be matched to the literal legend entry "Liberation Day" (day D3), "eleven hours" matched exactly to an entry in the hours legend (H4), and "at my desk" matched exactly to "at my desk" in the place legend (P1) — all three happened to be exact matches, so no nearest-entry judgment call was needed here, but the legend text explicitly warns that inexact matches should take the nearest entry and be recorded, which I'd have had to flag if any of the three hadn't matched cleanly.
