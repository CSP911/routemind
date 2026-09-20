1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body

2. **Answer**: 1.35x

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (established which version is in force for 2024-07-03)
- /v1/nodes/hard-overtime-v2/body (the table with the D2/H2 figure)

4. **Notes**: The walk started in payroll, since payroll's own overview says overtime premiums "moved to attendance on 2026-01-01" and the old rule is "still here" as `payslip-overtime`. That old payroll page (`/v1/nodes/payslip-overtime/body`) turned out to be a dead end for this question: it only gives flat +50%/+100% premiums with no day (D1..D4) or hour-band (H1..H4) breakdown at all, so it can't be the source of a "D2/H2" figure — this cost a few extra hops (payslip table → sec-payslip-lines-in-detail table) before realizing it. The real answer lives in attendance, which has its own three-version history for overtime, separate from payroll's two-version note. The legend document (`hard-overtime-legend-revision`) was essential: it explicitly says the oldest version's date range is "until 2024-07-01" and the second version is "2024-07-01 to 2025-12-31," which matches "two days after the first change" = 2024-07-03, i.e. two days into the v2 table taking effect on 2024-07-01. Without that legend it would have been easy to guess wrong — e.g., assume the newest three-qualifier `sec-hard-overtime` table applies just because it's "current," which the legend explicitly warns against. The v2 table's own qualifier count (two: day and hours) also matches the "day D2 ... hour band H2" phrasing in the question, confirming this was the right version before even checking dates.
