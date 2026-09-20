## Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body

## Answer

Accrues 1.26 days per month. Carry-over limit is 13 days — that is the most that can still be held into January.

## Source

- /v1/nodes/hard-accrual-legend-revision/body (confirms 2026-09-20 falls under the current, 2026-01-01-onward table)
- /v1/nodes/hard-accrual-legend-site/body ("fully from home" → site L4)
- /v1/nodes/hard-accrual-legend-tenure/body ("been here five years" → tenure T3, exact match)
- /v1/nodes/hard-accrual-legend-type/body ("in three days a week" → type E3, exact match)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body (the answer: 1.26 days/month accrual, 13-day carry-over limit)

## Notes

- The question's phrasing ("In three days a week... fully from home") maps directly onto the three legend tables' own wording almost verbatim — "in three days a week" is the literal type-E3 legend entry, not a description of a 3-day hybrid schedule as I first assumed. It's easy to misread this as "works from home, in office 3 days a week" and go hunting in flexible/remote-working docs instead of recognizing it as a legend qualifier for employment type. All three qualifiers (type, tenure, site) turned out to be exact legend matches, so no "nearest entry" judgment call was needed here.
- Had to check the legend-revision warning first since there are three superseded versions of the accrual table with different indexing (one/two/three qualifiers) — today's date (2026-09-20) falls under the current three-qualifier table (`sec-hard-accrual`, in force since 2026-01-01), so no ambiguity there, but it would have been a mistake to skip that check and just grab the newest-looking table without confirming the date range.
- "How much can I still be holding in January" reads like a separate question about a future entitlement, but it's actually just asking for the row's carry-over limit (13 days) — the same row answers both parts of the question at once.
