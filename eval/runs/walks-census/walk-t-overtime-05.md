1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body

2. **Answer**
1.35x (day D2, hour band H2, under the overtime rate version in force 2024-07-01 to 2025-12-31)

3. **Source**
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-v2/body

4. **Notes**
Started down the wrong branch: payroll's own note (`hard-moved-overtime`) says overtime premiums moved to attendance on 2026-01-01 and that the payroll page (`payslip-overtime`) is "the old rule, correct only before 2026-01-01." That phrasing makes it sound like `payslip-overtime` is the answer for any pre-2026 date, including March 2025. But `payslip-overtime` only has flat premiums (+50%/+100% by category) with no D-day or H-hour-band structure at all, so it can't answer a question phrased in terms of "day D2" and "hour band H2" — that was the tell that I had the wrong document.

The real structure lives in attendance, which has its own legend-revision page (`hard-overtime-legend-revision`) spelling out that overtime rate has been written THREE times, not two: pre-2024-07-01 (`overtime-rate-table`, one qualifier), 2024-07-01 to 2025-12-31 (`hard-overtime-v2`, two qualifiers: day and hours), and 2026-01-01 onward (`sec-hard-overtime`, three qualifiers, adds place). March 2025 falls in the middle version. The legend page explicitly flags this as the case worth being careful about — grabbing either the oldest or the current table is wrong. None of the three versions says it superseded the others, so date-checking against the legend page, not assumption, is what actually resolves it. Did not need to open `sec-hard-overtime` or `overtime-rate-table` once the date range confirmed `hard-overtime-v2` was the right one.
