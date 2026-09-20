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
- /v1/nodes/hard-overtime-legend-revision/body (identifies which of three versions covers October 2024)
- /v1/nodes/hard-overtime-v2/body (the table itself: D2 × H2 = 1.35x)

4. **Notes**:
This one had a real trap. Payroll's own overtime page (`/v1/nodes/payslip-overtime/body`) looked like the answer at first glance — payroll is the obvious place to look for pay multipliers, and its warning node (`hard-moved-overtime`) explicitly says the old payroll rule is "correct only before 2026-01-01," which would have made October 2024 look like a match. But that payroll page has no day/hour-band structure at all (no D1–D4, no H1–H4), so it can't be the source for "day D2, hour band H2" — it was a single flat +50%/+100% table, not indexed by day or hour. Taking it at face value would have given a confidently wrong non-answer.

The real structure lives in attendance, and it turns out overtime rates there have been rewritten three times, not two. The legend node (`hard-overtime-legend-revision`) is explicit that reaching for the newest ("current since 2026-01-01") is wrong for pre-2026 dates, and that the oldest version says nothing about being superseded — so without checking the legend first I could easily have grabbed `overtime-rate-table` (pre-2024-07-01, "one qualifier," no day/hour split at all) or `sec-hard-overtime` (current, three qualifiers including place) and gotten either a non-answer or a wrong-version answer. October 2024 falls in the 2024-07-01–2025-12-31 window, which is the middle version (`hard-overtime-v2`, "two qualifiers" = day and hours) — exactly the one the legend flags as the case where "taking either extreme is wrong." That table gives D2/H2 = 1.35x directly.
