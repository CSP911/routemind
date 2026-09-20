1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/nodes/payslip-overtime
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-overtime-and-hours
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body

2. **Answer**
+50% (a 1.5x multiplier) on the hourly basic pay rate for ordinary overtime beyond the 40-hour week, under the rule in force until 2024-07-01, which covers September 2023.

3. **Source**
/v1/nodes/hard-overtime-legend-revision/body (identifies which of three versions governs the date)
/v1/nodes/overtime-rate-table/body (the version in force until 2024-07-01, covering September 2023 — gives the +50% figure)

4. **Notes**
The payroll region's own overtime page (/v1/nodes/payslip-overtime/body) looked like a complete answer on its own: it states +50% for overtime and is explicitly flagged as "the old rule, correct only before 2026-01-01." Since September 2023 is before that cutoff, it would have been easy to stop there and report +50% straight from payroll. That would have been the right *number* by luck but for the wrong reason and from a source the question wasn't really pointing at — the payroll page doesn't distinguish between two different pre-2026 regimes.

Checking the attendance region turned up /v1/nodes/hard-overtime-legend-revision/body, which reveals the overtime rate was actually written three separate times: until 2024-07-01, 2024-07-01–2025-12-31 (a day/hour-indexed multiplier table, hard-overtime-v2, with values like 1.20x–1.65x), and 2026-01-01 onward. The legend explicitly warns that reaching for the newest version is wrong for pre-2026 dates, and that the 2024-07-01–2025-12-31 middle version is the one place where guessing an extreme (oldest or newest) fails. September 2023 falls in the oldest bracket, so the correct cited source is /v1/nodes/overtime-rate-table/body, not the payroll page and not hard-overtime-v2.

The oldest table and the payroll page happen to agree on the +50% figure for ordinary overtime, so the final number doesn't change — but the exercise made clear that payroll's page cannot be trusted as an authority on which version governs a given date; only the attendance legend page settles that, and it's easy to miss because payroll's own framing implies its single page covers everything before 2026-01-01.
