1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body
```

2. **Answer**
For type E2, tenure T2, site L3 (current table, in force from 2026-01-01): accrues 0.84 days per month. Carry-over limit is 9 days — that is the most you can still be holding into January.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which version applies to today's date, 2026-09-20)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body (the figures)

4. **Notes**
Leave accrual has three superseded/current versions indexed under different addresses (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the oldest one gives no indication it's been replaced. Checked the legend-revision page before reading the table to confirm 2026-09-20 falls under the current version (`sec-hard-accrual`, in force since 2026-01-01) rather than the 2024-07-01–2025-12-31 version — grabbing the newest-looking table without that check would have been the wrong instinct in general, even though it happened to be correct here. The question already gave the type/tenure/site codes directly, so the legend files (site/tenure/type) weren't needed. "How much can I still be holding in January" is answered by the carry-over limit field (9 days); the table doesn't spell out that this figure specifically governs what's held at year-end/into January, so that mapping required interpretation of the row's "carry-over limit" label rather than an explicit statement.
