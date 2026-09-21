1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For day D4, hours H3, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multiplier is a pay concept" --member /v1/regions/attendance "day/hour/place overtime rules might be defined alongside attendance"
./bench/rmcli.py overlay remove --id ov_2026-09-21_2e8f5a --address /v1/regions/payroll --why "warning file confirms overtime premiums moved to attendance on 2026-01-01, payroll no longer authoritative"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_2e8f5a --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body

2. **Answer**: Multiplier 2.88x; minutes rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime-rate versions is current for today's date, 2026-09-21)
- /v1/nodes/sec-hard-overtime (current overtime rate table, in force from 2026-01-01, listing the row for day D4/hours H3/place P1)
- /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p1/body (the answer: multiplier and rounding)

4. **Notes**: My first working set guessed the answer might be under payroll (overtime multiplier sounds like a pay figure), but a hard-moved-overtime warning file listed there said overtime premiums moved to attendance on 2026-01-01, so I dropped payroll and moved to attendance. There, the table names three separate overtime-rate documents (an old one, a 2024-07-01–2025-12-31 version, and the current one from 2026-01-01), and a revision-legend file makes clear the date on the question decides which applies — since it's 2026-09-21 and the question has no date of its own, the current table (`sec-hard-overtime`) was the right one, not the superseded `hard-overtime-v2`. The row itself was addressed exactly by day/hours/place codes (`hard-overtime-row-day-d4-hours-h3-place-p1`), so no legend lookups for what D4/H3/P1 mean were needed — the codes were given directly in the question.
