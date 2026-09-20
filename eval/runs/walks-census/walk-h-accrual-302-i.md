1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body

2. **Answer**
Accrues 1.40 days of leave per month. Carry-over limit is 6 days — that is the most that can still be held going into January.
(This is the current table, in force from 2026-01-01.)

3. **Source**
- /v1/nodes/hard-accrual-legend-type/body (mapped "here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "been here eight months" → tenure T1)
- /v1/nodes/hard-accrual-legend-site/body (mapped "in the Singapore entity" → site L3)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body (the figures: 1.40 days/month accrual, 6 days carry-over limit)

4. **Notes**
The three legend tables (type, tenure, site) all had exact, verbatim matches to the phrasing in the question ("here from our partner firm", "been here eight months", "in the Singapore entity"), so no nearest-entry judgment calls were needed here — that's unusually clean for this kind of walk. The one thing worth flagging: the accrual table is explicitly versioned (a current 2026-01-01 table plus two superseded versions, `hard-accrual-v2` and `leave-accrual`, per `hard-accrual-legend-revision`). I only read the current table since today's date (2026-09-20) falls within its effective range — but it would be easy to grab a superseded row by accident if not checking dates. "How much can still be holding in January" is answered by the row's "Carry-over limit" field; I read that as the ceiling on days held over the year-end into January, which is the most natural reading, but the question doesn't explicitly say "carry-over" so there's a small chance the asker meant something else (e.g. projected balance by January given current usage, which this table can't answer since it has no data on current balance or usage).
