1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body

2. **Answer**
You accrue 1.66 days of leave per month, and the carry-over limit — the most you can still be holding at the start of January — is 16 days.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirms today's date, 2026-09-20, falls under the current table, not an older version)
- /v1/nodes/hard-accrual-legend-type/body ("here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body ("been here nine years" → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body ("fully from home" → site L4)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body (final figures: 1.66 days/month, 16-day carry-over limit)

4. **Notes**
The question's phrasing ("here from our partner firm," "been here nine years," "fully from home") was clearly lifted verbatim from the three legend tables' left-hand columns — each phrase matched a legend row exactly, so no interpolation or "nearest entry" judgment call was needed. The one place this could easily go wrong is the date: the accrual subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page explicitly warns that reaching for the newest one is wrong for dates before 2026-01-01. Today (2026-09-20) is safely inside the current table's range, but I checked the revision page before committing to `sec-hard-accrual` rather than assuming. I read "how much can I still be holding in January" as asking for the carry-over limit (the cap on days held going into the new year), which the row states directly as 16 days — I did not find a separate, more specific "as of January" figure, so I'm treating the carry-over limit itself as the answer to that half of the question.
