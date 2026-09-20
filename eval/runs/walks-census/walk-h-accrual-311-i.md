## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body

## Answer
Accrues 1.46 days per month. Carry-over limit (how much you can still be holding into January) is 8 days.

## Source
- /v1/nodes/hard-accrual-legend-revision/body (established today, 2026-09-20, falls under the current table, not the two superseded versions)
- /v1/nodes/hard-accrual-legend-type/body (mapped "here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "been here two years" → tenure T2)
- /v1/nodes/hard-accrual-legend-site/body (mapped "at the Busan branch" → site L2)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body (final figures)

## Notes
The phrase "how much can I still be holding in January" isn't standard leave terminology — it reads at first like a request for a leave *balance*, which nothing in RouteMind could compute (no start date or usage history given). Re-reading it against the row's own field names, it lines up with "Carry-over limit" — the cap on what can still be held over into the new year — so I answered that rather than treating the question as unanswerable.

The three qualifying phrases in the question ("here from our partner firm," "been here two years," "at the Busan branch") matched their legend rows verbatim, word for word — E4, T2, L2. No nearest-entry judgment call was needed, which is the main way this walk could have gone wrong (the legends explicitly allow approximating to the nearest band when there's no exact match, and I'd have had to justify that choice here if it applied).

The one place I could have gone wrong outright: skipping /v1/nodes/hard-accrual-legend-revision/body and jumping straight to the current table without checking dates. The table listing at /v1/regions/attendance surfaces three separate accrual documents (oldest, a 2024-07-01–2025-12-31 version, and the current 2026-01-01 one) with no warning at that level that they coexist — the revision-legend document is what actually says the date decides which applies, and today's date (2026-09-20) confirms the current table (`sec-hard-accrual`) is correct.
