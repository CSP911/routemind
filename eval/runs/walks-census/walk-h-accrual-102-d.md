1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py read /v1/nodes/annual-leave/body

2. **Answer**
For type E2, tenure T1, site L3 (current table, in force from 2026-01-01, which is the one that applies to today's date 2026-09-20): accrues 0.76 days per month. Carry-over limit is 6 days — that is the most you can still be holding over into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (to confirm which of the three accrual versions applies to today's date)
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body (the figures: 0.76 days/month accrual, 6 days carry-over limit)

4. **Notes**
The attendance area's table flags up front that leave accrual has three superseded/current versions covering different date ranges (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and warns that the oldest page says nothing about being replaced — so grabbing the first accrual-looking document without checking the legend would silently give a wrong-era answer. Today (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct, and its row for E2/T1/L3 was a direct, unambiguous lookup.

The one place I nearly went wrong: the attendance area also holds a separate `/v1/nodes/annual-leave` document with its own accrual-like rules (grants on 1 January, unused days lapse and are paid out, no rollover). That document uses completely different mechanics — no type/tenure/site codes at all — and looks superficially relevant to "how much can I still be holding in January." It is not part of the type/tenure/site row system the question is phrased in, and mixing its "days lapse, don't roll over" framing with the hard-accrual table's "carry-over limit" field would produce a contradictory answer. I read it to confirm it was a different, non-applicable framework rather than a second source for the same figures.
