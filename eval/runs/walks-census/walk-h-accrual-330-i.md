1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. Answer

You accrue 1.60 days per month, and the carry-over limit is 13 days (the most you can still be holding once the year rolls over into January).

3. Source

/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body
/v1/nodes/hard-accrual-legend-revision/body (confirms the current table applies to today's date, 2026-09-20)

4. Notes

The three qualifiers in the question map to codes only via three separate legend files, none of which repeat the plain-language description found on the row itself — "here from our partner firm" only resolves to E4 by reading hard-accrual-legend-type verbatim, and it's an easy place to guess wrong (e.g. confusing "partner firm" with a contract worker, E2). Same for "nine years" → T4 and "Seoul office" → L1; the mapping tables use exact phrasing so I matched the question's wording to the legend's left column rather than inferring from category names. The bigger trap was the leave-accrual versioning: there are three superseded/current versions of this table (leave-accrual, hard-accrual-v2, sec-hard-accrual), and the legend-revision doc is explicit that reaching for the newest one is wrong for a question dated before 2026-01-01. Today is 2026-09-20, safely inside the current table's range, so no correction was needed here, but I checked the revision doc anyway before finalizing since the question's "how much can I still be holding in January" phrasing made me briefly wonder if a year-boundary rule change applied — it doesn't; the carry-over limit is simply a static field on the current row.
