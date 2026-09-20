1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body

2. **Answer**
Accrues 1.18 days of leave per month. The carry-over limit is 10 days — that is the most that can still be held going into January.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirms which of the three accrual versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-accrual-legend-type/body (maps "in three days a week" → type E3)
- /v1/nodes/hard-accrual-legend-tenure/body (maps "been here two years" → tenure T2)
- /v1/nodes/hard-accrual-legend-site/body (maps "fully from home" → site L4)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body (the row with the actual figures)

4. **Notes**
The legend-revision page was the thing worth pausing on: leave accrual has been rewritten three times, and the oldest version doesn't announce that it was superseded, so grabbing the first "leave accrual" hit without checking dates would have silently produced the wrong table. Today's date (2026-09-20) put this squarely in the current (2026-01-01-onward) table, `sec-hard-accrual`, so no real ambiguity there — but it's the kind of question where a walk in 2025 would go a different way entirely.

The other near-miss was the type legend: "been here two years" and "on a two-year contract" (type E2) sit right next to each other, and it would be easy to fuse the tenure detail ("two years") into the type axis and pick E2 instead of E3. The three qualifiers (type/tenure/site) are independent, and only "in three days a week" actually selects the type; "two years" belongs on the tenure axis only. All three of this person's descriptors ("three days a week," "two years," "fully from home") happened to match a legend row exactly, so no nearest-entry judgment call was needed here.

For "how much can I still be holding in January," I read this as the carry-over limit (10 days) — the cap on what survives into the new year — rather than a projection of accumulated balance, since no start-of-year or current balance was given to project from.
