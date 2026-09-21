1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D1, hours H2, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier and minute rounding likely a payroll rule" --member /v1/regions/attendance "day/hours/place classification for overtime may be defined in attendance"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_4ad4d1 --outcome answered --used /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body /v1/nodes/hard-overtime-legend-revision/body

2. **Answer**: Multiplier 1.32x; minutes are rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body
/v1/nodes/hard-overtime-legend-revision/body

4. **Notes**: The overtime rate subject has three versions with overlapping validity, and the current one (`sec-hard-overtime`, in force from 2026-01-01) is only correct because today's date (2026-09-20) falls after that cutoff — the legend-revision doc warns explicitly that reaching for the newest table is wrong for any date before 2026-01-01, and that the oldest version says nothing about being superseded, so skipping that check would have been an easy way to get a plausible-but-wrong answer for an older date. The row address matched the D1/H2/P1 qualifiers exactly as printed, so no guessing was needed there.