## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body

## Answer
Accrues 1.64 days per month. Carry-over limit is 15 days — that is the most you can still be holding once the new year (January) starts; anything over that is settled at 15 days unless an unavoidable excess is claimed with a written statement, decided by the budget holder.

## Source
- /v1/nodes/hard-accrual-legend-revision/body (confirmed the 2026-01-01 current table applies, since today is 2026-09-20)
- /v1/nodes/hard-accrual-legend-type/body (mapped "here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "nine years" → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body (mapped "Singapore entity" → site L3)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body (the figures: 1.64 days/month, 15-day carry-over limit)

## Notes
The three qualifiers in the question line up almost too neatly with the exact legend wording ("here from our partner firm" is a verbatim match for the E4 row, "been here nine years" verbatim for T4, "Singapore entity" verbatim for L3), so there was no ambiguity in picking the row — this walk was intentionally easy to key.

The one place I could have gone wrong was the version: there are three superseded/current tables for leave accrual (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the revision-legend page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls inside the current table's window, so `sec-hard-accrual` was correct, but I checked the legend page before assuming that rather than defaulting to whichever table sorted first.

"How much can I still be holding in January" is worded as if it were a distinct entitlement figure, but the table only exposes one number that answers it: the carry-over limit (15 days). I read it as "the cap on what carries into the new year" rather than a separate accrual amount — the row's own "If the figures are exceeded" section confirms 15 is a hard limit with a settlement/claim process for anything above it, which supports that reading.
