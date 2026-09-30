1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay create --question "In March 2025, what multiplier was paid for day D2 work in hour band H2? Answer under the version of the overtime rate that was in force on that date." --member /v1/nodes/hard-moved-overtime/body "confirms payroll's old overtime rule applies for dates before 2026-01-01, which covers March 2025" --member /v1/nodes/payslip "payslip table area in payroll, may link to payslip-overtime id with the old overtime rates"
./bench/rmcli.py overlay add --id ov_2026-09-20_e529a3 --address /v1/nodes/payslip-overtime/body --why "the old overtime rule document itself, effective pre-2026-01-01, covers March 2025"
./bench/rmcli.py overlay remove --id ov_2026-09-20_e529a3 --address /v1/nodes/nontaxable --why "not relevant to overtime multipliers" (failed: address not in overlay)
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay add --id ov_2026-09-20_e529a3 --address /v1/nodes/hard-overtime-legend-revision/body --why "explains which of three overtime rate versions covers which date range"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py overlay add --id ov_2026-09-20_e529a3 --address /v1/nodes/hard-overtime-v2/body --why "the version in force 2024-07-01 to 2025-12-31, which covers March 2025; indexed by two qualifiers matching D2/H2 coding"
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e529a3 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-v2/body

2. **Answer**: 1.35x

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (established that the 2024-07-01 to 2025-12-31 version, `hard-overtime-v2`, is the one in force for a March 2025 date)
- /v1/nodes/hard-overtime-v2/body (the table itself: D2 row, H2 column = 1.35x)

4. **Notes**: The obvious first path — payroll's `payslip-overtime` page — is a trap. It reads as a complete, current-looking overtime rule (flat +50%/+100% premiums, no day/hour-band structure at all), and nothing on the page itself says it's wrong for March 2025. Only the sibling `hard-moved-overtime` note in payroll flags that overtime premiums moved to attendance on 2026-01-01 — but even that note is misleading for this question: it frames payroll's page as "the old rule, correct only before 2026-01-01," which sounds like it should cover March 2025. It doesn't, because payroll's page was never the D2/H2-coded rule to begin with — the day/hour-band structure the question asks about only exists in attendance, which itself turned out to hold three superseded versions of the overtime table, not one. Without opening `hard-overtime-legend-revision` I would have grabbed the current `sec-hard-overtime` table (three qualifiers, current since 2026-01-01) and answered with the wrong-era multiplier. The legend page was the only thing that made the three-version split and the correct date range explicit.
