1. Commands
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner-firm employee, 9 years tenure, fully remote: monthly leave accrual rate and max carryover held in January" --member /v1/regions/attendance "leave accrual, carryover, and eligibility by tenure/work arrangement/employment type live here"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_55ff60 --outcome answered --used /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body

2. Answer
Accrues 1.66 days per month. Can hold (carry over) up to 16 days into January.

3. Source
/v1/nodes/sec-hard-accrual (table listing, current accrual table in force from 2026-01-01)
/v1/nodes/hard-accrual-legend-type/body (maps "here from our partner firm" → type E4)
/v1/nodes/hard-accrual-legend-tenure/body (maps "been here nine years" → tenure T4)
/v1/nodes/hard-accrual-legend-site/body (maps "fully from home" → site L4)
/v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l4/body (the row: 1.66 days/month accrual, 16-day carry-over limit)

4. Notes
The three qualifiers in the question ("partner firm", "nine years", "fully from home") each map to a legend table with near-exact wording matches to the row's own phrasing ("here from our partner firm" is even the row's own worked example text) — no fuzzy nearest-entry judgment calls were needed here, which is unusual and worth flagging as a place I double-checked rather than assumed. The one thing I verified rather than took for granted: the table is explicitly dated "in force from 2026-01-01," and the walk's date (2026-09-20/21) falls inside that window, so this is the correct version and not the superseded hard-accrual-v2 or the original leave-accrual — I did not need to open the legend-revision doc to resolve an ambiguity, but I did check the in-force date printed on the row itself before trusting it.
