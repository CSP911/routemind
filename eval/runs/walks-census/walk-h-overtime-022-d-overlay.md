1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H3, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers and pay rules are typically in payroll" --member /v1/regions/attendance "hours/day/place classification and time rules may be in attendance"
./bench/rmcli.py overlay remove --id ov_2026-09-20_4edf5a --address /v1/nodes/insurance --why "irrelevant, not about overtime"
./bench/rmcli.py overlay remove --id ov_2026-09-20_4edf5a --address /v1/nodes/payroll-desk --why "irrelevant"
./bench/rmcli.py overlay remove --id ov_2026-09-20_4edf5a --address /v1/nodes/payroll-overview/body --why "irrelevant"
./bench/rmcli.py overlay remove --id ov_2026-09-20_4edf5a --address /v1/nodes/payslip --why "irrelevant"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_4edf5a --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body

2. **Answer**: Multiplier is 1.50x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate versions applies given today's date, 2026-09-20)
- /v1/nodes/sec-hard-overtime (the current table, listing the row for day D1, hours H3, place P3)
- /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body (the row itself — multiplier and rounding)

4. **Notes**: The overtime subject has three superseded/current versions (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision doc explicitly warns that "the oldest says nothing at all about having been replaced" — so grabbing the first plausible-looking overtime table without checking the revision legend would have risked silently using stale rates. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-overtime`, indexed by three qualifiers: day/hours/place) was the correct one; a question dated in 2025 would have needed `hard-overtime-v2` instead. My initial overlay guessed the answer might live in payroll, but a hard-moved-overtime note (surfaced right in the first overlay listing) flagged that overtime premiums moved out of payroll into attendance on 2026-01-01, which matched what I found — the real answer was entirely under attendance. The four `overlay remove` calls on payroll rows failed with 404 (the addresses I tried to remove weren't actually registered as members under those exact strings), which cost a few wasted calls but didn't block finding the answer — the overlay close still went through fine using addresses reached via table/read rather than ones explicitly added as members.
