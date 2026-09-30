1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For something dated 3 July 2024 (two days after the first change), what multiplier was paid for day D2 work in hour band H2? Use the version in force on that day." --member /v1/regions/payroll "overtime multiplier by day/hour band is a payroll concept"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py overlay add --id ov_2026-09-20_3cc84b --address /v1/nodes/payslip-overtime --why "old overtime rule, correct for dates before 2026-01-01, per hard-moved-overtime note"
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py overlay remove --id ov_2026-09-20_3cc84b --address /v1/nodes/payslip-overtime --why "wrong address, not printed by any table; correct one is /v1/nodes/payslip-overtime/body"
./bench/rmcli.py overlay add --id ov_2026-09-20_3cc84b --address /v1/nodes/payslip-overtime/body --why "overtime premium multipliers by day/hour band, correct address as printed by sec-payslip-lines-in-detail"
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay remove --id ov_2026-09-20_3cc84b --address /v1/nodes/payslip-overtime/body --why "payroll overtime page has no D2/H2 band notation and predates the versioned attendance tables; wrong document"
./bench/rmcli.py overlay add --id ov_2026-09-20_3cc84b --address /v1/nodes/hard-overtime-legend-revision/body --why "explains which of the three overtime versions covers 3 July 2024"
./bench/rmcli.py overlay add --id ov_2026-09-20_3cc84b --address /v1/nodes/hard-overtime-v2/body --why "version in force 2024-07-01 to 2025-12-31, covers 3 July 2024"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_3cc84b --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-v2/body

2. **Answer**: 1.35x

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-v2/body

4. **Notes**: I initially went to /v1/regions/payroll, since "overtime multiplier" sounds like a payroll topic, and payroll even has a warning node (hard-moved-overtime/body) about overtime being moved to attendance on 2026-01-01 — which correctly implied the pre-2026 rule was "still here" in payroll under `payslip-overtime`. That was a dead end for two reasons: first, the address the warning table printed (`/v1/nodes/payslip-overtime`) wasn't a real address — I had to drill into `payslip` → `sec-payslip-lines-in-detail` to find the real one, `/v1/nodes/payslip-overtime/body`. Second, once read, that page turned out to be the wrong document entirely: it only lists flat premiums (overtime/night/holiday), with no D2/H2 day-by-hour-band matrix at all — nothing in it matches the question's vocabulary. The real document lives in /v1/regions/attendance, not payroll, despite the payroll warning page implying payroll was where the pre-2026 rule remained. Attendance's table revealed the actual versioned history: three overtime-rate documents (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), with a legend-revision page explicitly warning that the oldest version "says nothing at all about having been replaced" — exactly the trap I'd nearly fallen into by trusting the payroll page as if it were current for 2024. The legend page also confirmed the "two days after the first change" framing: the first change was the 2024-07-01 cutover, and the version in force from that date (indexed by "two qualifiers" — day and hour, matching D2/H2) is `hard-overtime-v2`, which directly gives D2×H2 = 1.35x.
