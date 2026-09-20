1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body

2. **Answer**
For type E3, tenure T3, site L2 (current table, in force since 2026-01-01):
- Accrues 1.22 days per month.
- Carry-over limit is 11 days — that is the most you can still be holding going into January.
(Note: this table also says leave does not accrue during unpaid leave, and any approved-in-advance excess above these figures is a separate claim process, not part of the base figures asked for.)

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body

4. **Notes**
The main risk here was version confusion, not the E3/T3/L2 lookup itself. The attendance area lists three
generations of the leave-accrual subject (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with a
warning page explicitly noting the oldest version "says nothing at all about having been replaced" — so
grabbing the first accrual-looking table found without checking the legend-revision page would silently
give a stale answer. Today's date (2026-09-20) falls after 2026-01-01, so the current table
(`sec-hard-accrual`) was correct, but this is exactly the kind of question where reaching for the newest
without checking is only right by luck.
Second point of possible confusion: the question asks "how much can I still be holding in January" —
this is not a separate lookup, it's asking about the row's "carry-over limit" field, which caps what
survives into the new year. It would be easy to misread this as a request for a different document (e.g.
something about year-end settlement) rather than recognizing it as the same row's carry-over figure.
