1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "How many times has the overtime rate been rewritten, and from what date does each version apply?" --member /v1/regions/payroll "overtime rate is a payroll concept"
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay add --id ov_2026-09-20_d729bc --address /v1/nodes/hard-overtime-legend-revision/body --why "explicit legend of overtime rate versions and their dates"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py overlay add --id ov_2026-09-20_d729bc --address /v1/nodes/payslip-overtime/body --why "the oldest version (until 2024-07-01), reached via payroll's payslip-lines table"
./bench/rmcli.py overlay close --id ov_2026-09-20_d729bc --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/payslip-overtime/body /v1/nodes/hard-overtime-v2/body /v1/nodes/sec-hard-overtime

2. **Answer**:
The overtime rate has been written three times (rewritten twice, on top of the original):
- Version 1 (original): in force until 2024-07-01. One qualifier only (premium type: overtime/night/holiday hours). Documented at /v1/nodes/payslip-overtime/body.
- Version 2 (first rewrite): in force from 2024-07-01 to 2025-12-31. Two qualifiers (day, hours). Documented at /v1/nodes/hard-overtime-v2/body.
- Version 3 (second rewrite, current): in force from 2026-01-01 onwards. Three qualifiers (day, hours, place). Documented at /v1/nodes/sec-hard-overtime.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-v2/body
/v1/nodes/sec-hard-overtime
/v1/nodes/payslip-overtime/body

4. **Notes**:
The natural first instinct was to stay in payroll, since "overtime rate" sounds like a pay topic, and payroll's own table even lists a `payslip-overtime` document. But payroll's `/v1/nodes/hard-moved-overtime/body` immediately flags that overtime premiums moved to attendance on 2026-01-01, and that the payroll page is only correct before that date — so a payroll-only search would have silently missed the two newer versions living in attendance.

The real trap was in attendance itself: `hard-overtime-legend-revision/body` explicitly warns that this subject has THREE versions, not two, and that "reaching for the newest is wrong for anything before 2026-01-01." It's easy to find `sec-hard-overtime` (labeled "THE CURRENT ... TABLE") and `hard-overtime-v2` and stop there, assuming two versions — missing that the pre-2024-07-01 rule is a third, older version that was never withdrawn and says nothing about being superseded. That oldest version isn't filed in attendance at all; it's the `payslip-overtime` document still sitting in payroll, which is the same "old rule" hard-moved-overtime pointed at. Only cross-referencing the legend's "indexed by one/two/three qualifiers" descriptions against payslip-overtime's single-qualifier (type-only) table confirmed the two documents describe the same version. Nothing in the knowledge base gave a single canonical address for that oldest version or an explicit start date for it — its effective start is simply "until 2024-07-01," open-ended backward.
