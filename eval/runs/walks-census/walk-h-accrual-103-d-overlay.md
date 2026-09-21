1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T1, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "accrual rate and carry cap depend on employment type, tenure, and site — attendance table"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py overlay add --id ov_2026-09-20_93bb74 --address /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body --why "exact row for type E2, tenure T1, site L4 in the current (2026-01-01 onward) accrual table"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_93bb74 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body

2. **Answer**: Accrues 0.78 days per month. Carry-over limit (the most that can be held/carried over) is 7 days.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (established which of the three accrual versions applies)
- /v1/nodes/sec-hard-accrual (current accrual table, located the specific row)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body (the figures used in the answer)

4. **Notes**: Leave accrual has three superseded/current versions keyed by date, and the legend page warns that the oldest version doesn't announce having been replaced — so I checked the revision legend before trusting any table. Today's date (2026-09-21) falls within the current table's in-force window (2026-01-01 onward), and the question's "January" also falls within that window, so there was no version-boundary ambiguity here — both the query date and the referenced month point to the same (current) table. The only mild ambiguity was interpreting "how much can I still be holding in January" as the carry-over limit rather than a literal balance projection; the row only exposes a static carry-over cap (7 days), not a month-by-month accrual schedule, so that cap is the only figure the source supports.
