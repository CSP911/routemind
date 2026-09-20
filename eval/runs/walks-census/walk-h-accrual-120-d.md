## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body

## Answer
For type E2, tenure T3, site L1 (current table, in force since 2026-01-01):
- Accrues 0.88 days per month
- Carry-over limit: 10 days — this is the most you can still be holding into January

## Source
- /v1/nodes/hard-accrual-legend-revision/body (confirmed today's date, 2026-09-20, falls under the current 2026-01-01 table, not the superseded versions)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body (the accrual and carry-over figures)

## Notes
There are three versions of the leave-accrual subject (pre-2024-07-01, 2024-07-01 to 2025-12-31, and current since 2026-01-01), and the region table for attendance lists all three side by side with similar-looking names (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`). It would be easy to grab the wrong one without first checking the legend-revision page, since the oldest version doesn't say anywhere that it's been superseded. Today's date (2026-09-20) clearly falls in the current-table window, so `sec-hard-accrual` was correct here, but this is the kind of question where jumping straight to a plausible-looking address without the date check would silently give a stale answer.

The three qualifiers (E2, T3, L1) were given directly in the question and matched an exact row address in the table listing, so no legend lookups (type/tenure/site) were needed to translate a person's situation into codes — the walk was shorter than it might have been for a less precisely specified question.

The phrase "how much can I still be holding in January" maps to the row's "Carry-over limit, days" field — read this as the cap on unused leave carried into the new year, not as a separate accrual-forecast calculation.
