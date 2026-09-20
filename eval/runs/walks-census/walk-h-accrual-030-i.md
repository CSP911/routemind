1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body

2. **Answer**
Accrues 0.64 days per month. Carry-over limit into January (the amount you can still be holding) is 13 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body

4. **Notes**
The attendance area lists three versions of the leave accrual subject (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly against reaching for the newest by default. Today's date (2026-09-20) falls after the current table's 2026-01-01 start, so `sec-hard-accrual` was the right pick — but this is exactly the kind of question where grabbing the current table without checking the revision page first would have worked by luck rather than by reasoning. Worth flagging: had the question been dated in 2025, the correct table would have been the superseded `hard-accrual-v2`, not this one.

All three qualifiers ("regular payroll" → E1, "nine years" → T4, "Seoul office" → L1) matched a legend row exactly, with no fuzzy "nearest entry" judgment needed — so no ambiguity there. The one place to be careful: the question asks "how much can I still be holding in January," which is the carry-over limit field, not the monthly accrual rate — the two numbers (0.64 and 13) are easy to conflate if skimming the row table quickly.
