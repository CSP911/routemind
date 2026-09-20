1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py read /v1/nodes/payslip-overtime
./bench/rmcli.py table /v1/nodes/payslip-overtime
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/nodes/payroll-desk
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/overtime-rate-table
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body

2. **Answer**: +50% (1.5x) for ordinary overtime beyond the 40-hour week.

3. **Source**: /v1/nodes/hard-overtime-legend-revision/body, /v1/nodes/overtime-rate-table/body

4. **Notes**: This one had a trap. Payroll's own page (`hard-moved-overtime`) says the overtime rule "still here" in payroll (`payslip-overtime`) is "the old rule, correct only before 2026-01-01" — and `payslip-overtime` does list ordinary overtime at +50%, which happens to match the right answer here, but for the wrong reason. If I'd stopped there I'd have gotten the right number off a page that doesn't actually know about 29 June 2024 specifically — it just claims to cover everything before 2026-01-01, no mention of any earlier change.

The real picture only showed up in attendance: `hard-overtime-legend-revision` says overtime rate has been written **three times** — until 2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward. 29 June 2024 is two days before the first cutover (2024-07-01), matching the question's "two days before the first change" framing exactly, so the applicable version is the oldest one, `overtime-rate-table` (not `payslip-overtime` in payroll, and not `hard-overtime-v2`, which replaces it with a day/hour-indexed multiplier grid that has nothing at +50%). The payroll page's blanket "old rule, correct only before 2026-01-01" is misleading in isolation — it ignores the intermediate version entirely and would give the right multiplier here only by coincidence, since `overtime-rate-table` and `payslip-overtime` happen to agree on this one figure. Had the date landed between 2024-07-01 and 2025-12-31, trusting payroll's page instead of the attendance legend would have given a completely wrong answer (a day/hour multiplier from `hard-overtime-v2` instead of a flat +50%).

One address, `overtime-rate-table`, was taken verbatim from the "where" column of the legend table rather than from a table/read listing — it wasn't printed as a full path anywhere, but `/v1/nodes/<id>` matched the pattern of every other address seen in this walk (e.g. `hard-overtime-v2`), and it resolved correctly.
