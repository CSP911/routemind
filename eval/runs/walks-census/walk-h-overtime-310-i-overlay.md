1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two in the morning, three hours, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime hours/night work tracking likely here" --member /v1/regions/payroll "overtime pay multiplier and minute rounding likely here"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_970a89 --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body

2. **Answer**: Multiplier 2.76x. Minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body

4. **Notes**: The three qualifiers in the question map onto three separate legend tables rather than one lookup — "two in the morning" is itself a day-type entry (day D4), which is easy to misread as a time-of-day detail belonging under an hours or place legend rather than the day axis. "three hours" maps to hours band H2 (whose anchor value is actually "three hours" verbatim), and "at my desk" maps to place P1. Only after resolving all three separately does the row address (day-d4-hours-h2-place-p1) assemble. I nearly stopped after the payroll region's `hard-moved-overtime` note, which warns overtime premiums moved out of payroll into attendance on 2026-01-01 — that pointed correctly toward `sec-hard-overtime` under attendance rather than any payroll table, and there is a decoy `hard-overtime-v2` (superseded, 2024-07-01 to 2025-12-31) that would give a wrong multiplier/rounding if the legend-revision warning were skipped; I used the current `sec-hard-overtime` table (in force since 2026-01-01), consistent with today's date. The overlay close reported all four used addresses as "reached" rather than matched members, since I only added the two region tables as overlay members and drilled down manually rather than adding each leaf address individually — not an error, just a byproduct of not calling overlay add at each hop.
