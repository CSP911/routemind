1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "2am, ~90 minutes, from home: what overtime multiplier applies, and to what rounding are minutes taken?" --member /v1/regions/attendance "overtime hours/rules, night work likely covered here" --member /v1/regions/payroll "overtime pay multiplier and rounding likely defined in payroll"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8b3746 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4/body

2. **Answer**: Multiplier is 2.73x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p4/body

4. **Notes**: The three legends have to be read before the row address can even be built — "two in the morning" maps to day D4 (not what I'd have guessed, since it reads like a time-of-day qualifier rather than a day-type one; the legend is explicit that it's the only place this mapping is written), "about ninety minutes" maps to hours H1, and "from home" maps to place P4 (distinct from "on standby at home" = P3, which is a trap for this exact phrasing). Easy to jump straight to a row guess without reading all three legends carefully — the day-code table especially reads oddly since none of its other examples are times. Confirmed the current table (`sec-hard-overtime`, in force from 2026-01-01) is the right version for today's date (2026-09-21) rather than one of the two superseded versions flagged in `hard-overtime-legend-revision`, so I didn't need to open that revision-warning document. The overlay's close command reported the four addresses I named as "reached ... from somewhere the overlay never named" — expected, since I only added the two region-level members up front and drilled into child tables/rows myself rather than adding each intermediate address to the overlay.
