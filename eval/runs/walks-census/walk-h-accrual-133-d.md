1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body

2. **Answer**
For type E2, tenure T4, site L4 (current table, in force since 2026-01-01): accrues 1.02 days of leave per month, with a carry-over limit of 16 days — that is the most you can still be holding into January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body

4. **Notes**
The attendance table warns up front that leave accrual has three versions with different date ranges (`hard-accrual-legend-revision`, `hard-accrual-v2`, and the current `sec-hard-accrual`). Today is 2026-09-20, which falls under the current table (in force from 2026-01-01), so I went straight there and didn't need to open the superseded versions — but it would have been easy to grab a stale row if I'd picked the wrong one without checking dates. The question already gave the codes E2/T4/L4 directly, so I skipped the legend files (type/tenure/site) — no translation was needed. The "how much can I still be holding in January" phrasing isn't a separate figure; it maps onto the row's "Carry-over limit" field, which is the only balance-cap number this row exposes.
