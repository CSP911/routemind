1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body

2. **Answer**
Accrues 0.68 days per month. Carry-over limit (how much can still be held into January) is 15 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (version check)
/v1/nodes/hard-accrual-legend-type/body (regular payroll → E1)
/v1/nodes/hard-accrual-legend-tenure/body (nine years → T4)
/v1/nodes/hard-accrual-legend-site/body (Singapore entity → L3)
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body (figures: 0.68 days/month, carry-over limit 15 days)

4. **Notes**
The legend-revision page is the trap here: leave accrual has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and current from 2026-01-01), and the oldest version "says nothing at all about having been replaced." Today's date (2026-09-20) put this squarely in the current table (`sec-hard-accrual`), but it would be easy to grab the first accrual-looking node without checking dates. Also had to resist reading the carry-over limit as a separate "January" rule — the question's "how much can I still be holding in January" is just plain-language for the row's "Carry-over limit, days" field, not a distinct year-end/January-specific policy; there was no separate January-dated node in the table that would have been a better match, so I'm confident this is the right field rather than a coincidental resemblance.
