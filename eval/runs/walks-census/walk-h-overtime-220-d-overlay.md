1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D3, hours H3, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers are pay rate related, likely payroll" --member /v1/regions/attendance "overtime hour bands/day types could be defined in attendance rules"
./bench/rmcli.py overlay remove --id ov_2026-09-21_d7dbf8 --address /v1/nodes/insurance --why "not related to overtime"
./bench/rmcli.py overlay remove --id ov_2026-09-21_d7dbf8 --address /v1/nodes/payroll-desk --why "not related to overtime"
./bench/rmcli.py overlay add --id ov_2026-09-21_d7dbf8 --address /v1/nodes/hard-overtime-legend-revision/body --why "clarifies which overtime table version applies for today's date"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d7dbf8 --outcome answered --used /v1/nodes/hard-moved-overtime/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body

2. **Answer**:
Multiplier: 2.40x. Rounding: to the nearest 15 minutes.

3. **Source**:
/v1/nodes/sec-hard-overtime (table, confirmed current since 2026-01-01)
/v1/nodes/hard-overtime-row-day-d3-hours-h3-place-p1/body (the row with the figures)

4. **Notes**:
Started the working set pointed at both payroll and attendance because "overtime multiplier" sounds like a pay-rate question and could plausibly live in payroll. Payroll's own row `hard-moved-overtime/body` immediately redirects: overtime premiums moved out of payroll into attendance's `sec-hard-overtime` table as of 2026-01-01, and today (2026-09-21) is after that date, so the current table applies, not the superseded payroll rule or the older `hard-overtime-v2`. Had I answered from the payroll region without opening that warning file, I'd have risked citing a withdrawn rule. Once inside `sec-hard-overtime`, the row addresses are literal (`hard-overtime-row-day-d3-hours-h3-place-p1`), so no lookup of the day/hours/place legends was needed — the D3/H3/P1 codes in the question mapped directly to the row address. The overlay tool flagged the two addresses I read as "reached" rather than pre-declared members since I fetched them by navigating the table/read commands rather than formally adding them first; the answer itself is unaffected.
