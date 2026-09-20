## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/nodes/payslip
./bench/rmcli.py table /v1/nodes/sec-payslip-lines-in-detail
./bench/rmcli.py read /v1/nodes/payslip-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body

## Answer
1.35x — the multiplier for day type D2, hour band H2, under the overtime rate version in force from 2024-07-01 to 2025-12-31, which covers August 2025.

## Source
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-v2/body

## Notes
Started in payroll (the region the question's wording — "overtime rate" — points to naturally), and found `payslip-overtime`, a plausible-looking table of flat premiums (+50%, +100%) with no day/hour breakdown at all. That page doesn't use "day D2" or "hour band H2" terminology, so it couldn't actually answer the question, but it would be easy to stop there and force-fit an answer since it's the only "overtime" table in payroll. The `hard-moved-overtime` note in payroll only pointed forward to the 2026-01-01+ table in attendance (`sec-hard-overtime`), not to any 2025 version — so following that pointer naively would have led to the wrong (current, three-qualifier) table for a 2025 date.

The actual fork is in attendance, which has three historical versions of the overtime rate, not two. The `hard-overtime-legend-revision` page is explicit that a 2025 date needs the *middle* version (`hard-overtime-v2`, indexed by day + hours — matching "D2"/"H2"), not the oldest (no day/hour breakdown) and not the current one (adds a third qualifier, place). Grabbing `sec-hard-overtime` because it's labeled "current" and "THE CURRENT ... TABLE" would have been the natural mistake for an August 2025 question — the table's own legend page calls this out directly as the case where "taking either extreme is wrong."
