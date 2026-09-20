## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body

## Answer
Accrues 1.20 days of leave per month. The carry-over limit is 10 days — that is the most you can still be holding into January.

## Source
- /v1/nodes/hard-accrual-legend-revision/body (confirms the current, 2026-01-01-onward table applies to a question dated 2026-09-20)
- /v1/nodes/hard-accrual-legend-site/body (Seoul office → site L1)
- /v1/nodes/hard-accrual-legend-tenure/body (five years → tenure T3)
- /v1/nodes/hard-accrual-legend-type/body (three days a week → type E3)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body (1.20 days/month accrual, 10-day carry-over limit)

## Notes
Accrual has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly against grabbing the newest without checking the date. Today (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct — but this is the exact trap the walk is built to catch, so I read the revision notice before touching the row.

All three qualifiers ("three days a week," "been here five years," "at the Seoul office") matched a legend row exactly — no nearest-entry judgment call was needed, which removed one likely source of error. The main ambiguity is interpreting "how much can I still be holding in January" as the row's "carry-over limit" field; the table doesn't use the word "January" anywhere, so this is a reasonable but inferred mapping from the row's carry-over figure to the user's phrasing, not a literal match.
