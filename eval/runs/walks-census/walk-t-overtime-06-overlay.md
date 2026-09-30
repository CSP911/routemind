1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In August 2025, what multiplier was paid for day D2 work in hour band H2? Answer under the version of the overtime rate that was in force on that date." --member /v1/regions/payroll "overtime rate multipliers by day type and hour band are payroll policy"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay add --id ov_2026-09-20_59d5dd --address /v1/nodes/payslip --why "the old overtime rule payslip-overtime lives under payslip table, correct for dates before 2026-01-01"
./bench/rmcli.py read /v1/nodes/payslip-items/body
./bench/rmcli.py read /v1/nodes/sec-payslip-lines-in-detail (table)
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py read /v1/nodes/payslip-payment-lines/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay add --id ov_2026-09-20_59d5dd --address /v1/regions/attendance --why "true versioned overtime table (D2/H2 codes, three revisions) lives here, not in payroll's payslip-overtime page"
./bench/rmcli.py overlay remove --id ov_2026-09-20_59d5dd --address /v1/nodes/payslip --why "payslip-overtime uses a different old naming scheme (overtime/night/holiday) not D2/H2 codes; attendance's versioned table is the actual match for this question's terminology"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_59d5dd --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-v2/body

2. **Answer**: 1.35x

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (established that the 2024-07-01–2025-12-31 version, `hard-overtime-v2`, governs an August 2025 date)
- /v1/nodes/hard-overtime-v2/body (the table itself: D2 × H2 = 1.35x)

4. **Notes**:
The walk started in payroll, which is where the question's subject (overtime multipliers) naturally lives, and payroll even has a page titled "Overtime, night and holiday premiums" (`payslip-overtime`) with a warning (`hard-moved-overtime`) saying the old rule there is "correct only before 2026-01-01." Since August 2025 is before that cutover, it looked like `payslip-overtime` was the answer. But that page's rates are keyed by category (overtime/night/holiday, +50%/+100%) with no D2 or H2 codes anywhere — it doesn't match the question's vocabulary at all. That was the near-miss: trusting the "correct before 2026-01-01" framing from `hard-moved-overtime` without checking whether the destination page actually used the terms in the question.

Backing out to `/v1/regions/attendance` turned up a second, separate versioning scheme just for overtime: `overtime-rate-table` (before 2024-07-01, no day/hour qualifiers), `hard-overtime-v2` (2024-07-01 to 2025-12-31, two qualifiers — day and hour band, i.e. D and H codes), and `sec-hard-overtime` (2026-01-01 onward, three qualifiers, adds place). The legend-revision page for this scheme explicitly warns that for a 2025 date "the answer is the middle one, not the oldest and not the current table" — which is exactly the trap: `hard-moved-overtime` in payroll only describes a single 2026-01-01 cutover and says nothing about a mid-2024 boundary, so relying on payroll's framing alone would have missed that a 2025 date sits in the *middle* of a three-version history, not just before-or-after a single one. `hard-overtime-v2` was the one table that both covered August 2025 and used D-day/H-hour-band notation, giving D2/H2 = 1.35x directly.
