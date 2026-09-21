1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D3, hours H1, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers and rounding rules are payroll-related" --member /v1/regions/attendance "day/hour/place codes could relate to attendance/overtime rules"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_300c5e --address /v1/nodes/hard-moved-overtime/body --why "superseded pointer, not the data"
./bench/rmcli.py overlay remove --id ov_2026-09-21_300c5e --address /v1/nodes/hard-overtime-v2/body --why "superseded version, question is dated 2026-09-20/21"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_300c5e --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body

2. **Answer**: Multiplier 2.22x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p3/body

4. **Notes**: This subject has three superseded/current versions of the overtime table (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision page is explicit that reaching for the newest is only correct for dates on or after 2026-01-01 — today (2026-09-21) qualifies, so `sec-hard-overtime` was the right pick, but it would have been easy to skip that check and grab the wrong version. The current table is indexed by exactly three qualifiers (day, hours, place) and has a pre-built row for every D×H×P combination, including an exact match for D3/H1/P3, so no interpolation or legend lookup was actually needed once the row was found — I had pulled in the day/hours/place legend files as overlay members but never had to read them since the row address itself already spelled out the combination unambiguously. The two remove calls on already-nonmember addresses each errored with HTTP 404 ("not in this overlay") — those two files were never actually added as members in the first place (only the two /v1/regions/payroll and /v1/regions/attendance table addresses were), so the remove commands were no-ops/mistakes on my part, not a tool problem.
