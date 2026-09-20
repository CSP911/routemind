## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body

## Answer
Accrues 0.88 days per month. Carry-over limit is 10 days — the most that can still be held (e.g. into January).

## Source
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body

## Notes
The attendance area lists three versions of the leave accrual subject (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) and warns that reaching for the newest by default is wrong for older dates. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`, three qualifiers) is correct here — but this was a real branch point, not a formality, and had to be checked against the legend-revision page rather than assumed. The three qualifiers (type/tenure/site) each needed their own legend lookup since the row addresses use codes (E2/T3/L1) that aren't guessable from the plain-language description — e.g. "two-year contract" maps to E2, not to a contractor/temp code one might guess. The row itself answered both halves of the question (monthly accrual and carry-over limit) in one document, so no further lookup was needed — I read "how much can I still be holding in January" as asking about the carry-over limit, since that's the figure governing what balance survives into the new year; there was no separate "January" or year-end-specific rule found in this row.
