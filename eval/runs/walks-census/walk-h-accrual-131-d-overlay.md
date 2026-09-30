1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T4, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual and carry-over/cap questions live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a29258 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body

2. **Answer**
For type E2, tenure T4, site L2 (current table, in force from 2026-01-01):
- Accrues 0.98 days per month.
- Carry-over limit is 14 days — that is the most you can still be holding into January.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirms today's date, 2026-09-20, falls under the current version of the table, not the superseded v2 or original)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body (the row with the monthly accrual rate and carry-over limit)

4. **Notes**
Leave accrual has three versions in RouteMind indexed by different numbers of qualifiers (one, two, three), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) is safely inside the current version's range (2026-01-01 onwards), so this wasn't a close call, but it was worth checking rather than assuming — the question gives exactly three qualifiers (type, tenure, site), which matches `sec-hard-accrual`'s indexing and made it easy to jump straight there, but the date is what actually decides the version, not the qualifier count.

One oddity: `overlay close` reported both used addresses as "reached" rather than as named overlay members, with a note that "reached" means "answered from somewhere the overlay never named." Both addresses were in fact rows/members of the overlay printed at creation, so this label seems to be a quirk of the tool rather than a sign I strayed from the working set — flagging it in case it means something I'm not seeing.

The question's second half ("how much can I still be holding in January") is a plain-language phrasing of "carry-over limit" — there's no separate January-specific figure in this table, just the one carry-over cap that applies going into the new year.
