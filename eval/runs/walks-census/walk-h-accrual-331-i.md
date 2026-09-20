## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body

## Answer
Accrues 1.62 days of leave per month. Carry-over limit (the most you can still be holding going into January) is 14 days.

## Source
- /v1/nodes/hard-accrual-legend-type/body (mapped "here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "been here nine years" → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body (mapped "at the Busan branch" → site L2)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body (accrual rate and carry-over limit)

## Notes
The three qualifiers in the question (partner firm, nine years, Busan) map cleanly and exactly onto rows in the three legend tables — no fuzzy "nearest entry" judgment call was needed, which is unusual and worth flagging since these legends explicitly anticipate imprecise matches. The main risk was the leave-accrual versioning: /v1/regions/attendance lists three versions (a legend-revision file, a superseded v2 table, and the current `sec-hard-accrual` table effective 2026-01-01), and today's date (2026-09-20) falls under the current version, so `sec-hard-accrual` was the correct pick. It would have been easy to grab the superseded `hard-accrual-v2` row by mistake since it's listed right alongside the current one with a similar name. I did not open the legend-revision file since the current table's own effective-date note (2026-01-01) already confirmed it covers today; that felt like enough but is worth double-checking if the answer looks off. "How much can I still be holding in January" is read here as the carry-over limit (14 days) — the maximum balance that survives into the new year — not a separate January-specific accrual figure, since no such figure exists in this row.
