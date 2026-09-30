1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D2, hours H2, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers and rounding rules are typically payroll policy"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_28c4f9 --address /v1/nodes/payroll-desk --why "overtime moved out of payroll, not relevant"
./bench/rmcli.py overlay add --id ov_2026-09-20_28c4f9 --address /v1/regions/attendance --why "hard-moved-overtime notice: overtime premiums now set in attendance table sec-hard-overtime"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_28c4f9 --address /v1/nodes/hard-overtime-v2/body --why "superseded version, question has no date so current table applies"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_28c4f9 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body

2. **Answer**: Multiplier 1.89x; minutes rounded to the nearest 10 minutes.

3. **Source**:
- /v1/nodes/hard-moved-overtime/body (routed away from payroll to attendance)
- /v1/nodes/hard-overtime-legend-revision/body (confirmed current table applies, no date given in question)
- /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body (the answer)

4. **Notes**: Started in payroll since overtime multipliers sound like a payroll question, but payroll's own top hit (`hard-moved-overtime`) redirects overtime premiums to attendance's `sec-hard-overtime` table for anything dated 2026-01-01 onward — starting in payroll would have been a dead end if I'd trusted the region name alone. Also had to check `hard-overtime-legend-revision`: this subject has three versions by date, and the question gives no date, so I treated it as asking about the current rules (today is 2026-09-21, table in force since 2026-01-01) rather than either superseded version. Two `overlay remove` attempts failed with 404 because I tried to remove addresses not yet actually in the overlay (the printed table apparently lists the full candidate set, not exactly my active members) — had to drop those remove calls and just add/read forward. The final row address was printed directly in the `sec-hard-overtime` table listing, so no guessing was needed.
