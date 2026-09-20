## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body

## Answer
Accrues 1.48 days of leave per month. The carry-over limit is 9 days — that is the most that can still be held into January.

## Source
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body

## Notes
The biggest trap was the three superseded versions of the accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`). Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct — but a careless reader could grab the legend-revision warning's example (which is about 2025 dates needing the middle version) and misapply it here. Worth double-checking the in-force date on the row itself, which confirms 2026-01-01 onward.

The three qualifiers also needed careful translation from the user's own words via the legends rather than guessing: "here from our partner firm" is not an obvious synonym for "type E4" (it's easy to mistake it for a contractor type, i.e. E2's "two-year contract," especially since the user also happens to have two years of tenure — that's a coincidence between the tenure legend's T2 wording and the E2 type label that could cause someone to pick the wrong type). "Been here two years" maps cleanly to tenure T2. "Singapore entity" maps to site L3, not to be confused with the similarly-worded "at the Seoul office" (L1) skimmed quickly.

The carry-over limit (9 days) is what answers "how much can I still be holding in January" — it's the cap on days carried into the new year, not an accrual figure, and it sits in the same row as the monthly rate so no second lookup was needed.
