1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body

2. **Answer**:
The overtime rate has been written three times (rewritten twice after the original):
- Version 1 (original): in force until 2024-07-01 — `overtime-rate-table` (payroll)
- Version 2 (first rewrite): in force 2024-07-01 to 2025-12-31 — `hard-overtime-v2` (attendance)
- Version 3 (second rewrite, current): in force from 2026-01-01 onwards — `sec-hard-overtime` (attendance)

3. **Source**:
- /v1/regions/payroll (table)
- /v1/nodes/hard-moved-overtime/body
- /v1/regions/attendance (table)
- /v1/nodes/hard-overtime-legend-revision/body

4. **Notes**:
The trail starts in payroll, where the overtime page looks current but is flagged as moved to
attendance as of 2026-01-01. That note (`hard-moved-overtime`) already lists all three versions
and their date ranges, so it would have been possible to stop there — but it explicitly points to
`hard-overtime-legend-revision` in attendance as "the full version table," so I followed that
instead of trusting the secondary summary. The two sources agree exactly on the three date ranges
and locations, so there's no discrepancy, just redundant confirmation. The trap flagged in both
pages: the oldest version (payroll's `overtime-rate-table`) never says it was superseded, so a
naive search that stops at the first plausible-looking payroll page would silently return a rule
that's been dead since 2024-07-01. Also worth flagging — I did not open `overtime-rate-table`,
`hard-overtime-v2`, or `sec-hard-overtime` themselves, since the question only asks how many times
the rate was rewritten and from what dates each version applies, which the legend page answers
directly without needing the rate tables' contents.
