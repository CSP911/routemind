## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/sec-hard-accrual/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
```

## Answer

Qualifiers: "two-year contract" → type E2; "nine years" service → tenure T4; "fully from home" → site L4.

- Accrues per month: **1.02 days**
- Carry-over limit (max you can still be holding into January): **16 days**
- (Also on this row, not asked but adjacent: notice required 3 working days; does not accrue during unpaid leave.)

## Source

- /v1/nodes/hard-accrual-legend-type/body
- /v1/nodes/hard-accrual-legend-tenure/body
- /v1/nodes/hard-accrual-legend-site/body
- /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body
- /v1/nodes/hard-accrual-legend-revision/body (used to confirm the current, 2026-01-01-onwards table is the right version for a 2026-09-20 question, not `hard-accrual-v2` or `leave-accrual`)

## Notes

- The accrual table has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each indexed by a different number of qualifiers (one, two, three). It would have been easy to grab a stale row from `hard-accrual-v2` since it's still sitting right there in the region table with no obvious "don't use this" flag until you open the legend-revision doc. Checked it explicitly: today's date (2026-09-20) falls under the current table (2026-01-01 onwards), so `sec-hard-accrual` is correct.
- The three qualifiers (type/tenure/site) are each resolved through a *separate* legend document, and none of the legends repeat the row codes for the other two dimensions — so you can't skip any of the three lookups. "Two-year contract" mapping to "type E2" was not obvious from the row address alone; had to read the legend to be sure it wasn't, say, mapped by contract duration under tenure instead.
- The question's "how much can I still be holding in January" is answered by the row's "carry-over limit" field, not by any separate document about carryover — worth noting because at first glance it looked like it might need a distinct lookup (e.g. a carryover-cap section under `sec-days-that-decide-money`), but the accrual row itself already carries that figure alongside the monthly rate.
