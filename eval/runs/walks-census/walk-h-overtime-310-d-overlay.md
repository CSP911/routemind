1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D4, hours H2, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-legend-revision/body "warning about which overtime version covers which dates"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_4fd332 --outcome answered --used /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body

2. **Answer**: Multiplier 2.76x; minutes are rounded to the nearest 10 minutes. (This row is in force from 2026-01-01, current as of today 2026-09-21.)

3. **Source**: /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body

4. **Notes**: Straightforward walk. The attendance area table flagged that overtime rate has three versions (a legend-revision warning node), so I deliberately added that legend node to the working set to check for a date trap before trusting the row — but the row itself states plainly it's "in force from 2026-01-01" and today is 2026-09-21, so the current table (`sec-hard-overtime`) was the right one with no need to fall back to the superseded `hard-overtime-v2` or `overtime-rate-table` versions. The one odd note: closing the overlay reported the address as "reached" rather than a named member, even though it was listed as a child row under the `/v1/nodes/sec-hard-overtime` table member in the overlay printout — seems to be how the tool distinguishes group members from individually-added addresses, not an error.
