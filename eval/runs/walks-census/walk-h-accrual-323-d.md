1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body

2. **Answer**
For type E4, tenure T3, site L4 (current table, in force since 2026-01-01):
- Accrues 1.58 days per month.
- Carry-over limit is 13 days — this is the most you can still be holding in January.
(Also noted: 5 working days' notice required to book leave; does not accrue during unpaid leave.)

3. **Source**
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body

4. **Notes**
Three versions of the leave accrual table exist (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns the oldest version never says it was superseded — it would be easy to land on it by accident. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is the right one; no ambiguity here since the question didn't specify a date, but it's the kind of check that's easy to skip. The question's codes (E4, T3, L4) matched the row-naming scheme exactly, so no detour through the site/tenure/type legends was needed — a person phrasing the question in plain language would have needed those legends to map their words to codes, but that wasn't required here. The row bundles carry-over limit alongside the monthly rate, which directly answers "how much can I still be holding in January" without needing a separate lookup.
