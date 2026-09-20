1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body

2. **Answer**
Accrual: 0.40 days per month.
Carry-over limit (max that can still be held into January): 4 days.
(Also: 2 working days' notice required to book; does not accrue during unpaid leave.)

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (established 2026-09-20 falls under the current, 2026-01-01-onward table, not the superseded versions)
/v1/nodes/hard-accrual-legend-type/body (regular payroll → type E1)
/v1/nodes/hard-accrual-legend-tenure/body (eight months → tenure T1)
/v1/nodes/hard-accrual-legend-site/body (Seoul office → site L1)
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body (final figures: 0.40 days/month accrual, 4-day carry-over limit)

4. **Notes**
The area index (`/v1/regions/attendance`) lists three separate leave-accrual write-ups (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with only a warning file distinguishing them — it would have been easy to grab the first plausible-looking accrual table without checking dates. The legend-revision doc makes clear the current table only governs from 2026-01-01, and today (2026-09-20) falls in that window, so `sec-hard-accrual` was the right pick over the two superseded versions.
The 64-row table is indexed by three separate legends (type/tenure/site) rather than plain language, and each legend explicitly warns "if what you have is not listed, take the nearest entry" — in this case all three inputs (regular payroll, eight months, Seoul) matched a legend row exactly, so no nearest-entry judgment call was needed, but it's the kind of table where skipping the legends and guessing a row address would silently give wrong numbers.
"How much can I still be holding in January" reads like it might be asking about a separate carryover/expiry policy elsewhere in Attendance, but the row itself already states a "Carry-over limit, days: 4" field, which directly answers it — no need to chase a second document.
