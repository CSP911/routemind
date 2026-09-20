1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**: For type E1, tenure T1, site L2: you accrue 0.42 days of leave per month. The carry-over limit is 5 days — that is the most you can still be holding into January (any excess not approved in advance is forfeited).

3. **Source**:
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body
/v1/nodes/hard-accrual-legend-revision/body

4. **Notes**: The row address at `/v1/nodes/sec-hard-accrual` already spelled out type/tenure/site in its address (`hard-accrual-row-type-e1-tenure-t1-site-l2`), so no separate legend lookup was needed to map E1/T1/L2 to a row — the three qualifiers named in the question matched the address directly. The near-miss was on dates: this domain has three different accrual tables (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) for different periods, and the legend-revision page warns that reaching for the newest is wrong for dates before 2026-01-01. Today is 2026-09-20 and the current table is in force from 2026-01-01 onward with no end date, so it also covers the next January — but I checked the revision page explicitly rather than assuming, since "how much can I still be holding in January" could have been read as asking about a boundary where the table might change. It doesn't rename the carry-over concept as "holding into January" explicitly — I inferred that "how much can I still be holding" maps to the "Carry-over limit" field, which was the only figure in the row that describes a cap on standing balance rather than a monthly flow.
