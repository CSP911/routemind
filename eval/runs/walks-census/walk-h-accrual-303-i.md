1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body

2. Answer
Accrues 1.42 days per month. Carry-over limit (the most that can still be held into January) is 7 days.

3. Source
/v1/nodes/hard-accrual-legend-revision/body (confirms the current, 2026-01-01-onward table applies to a 2026-09-20 question)
/v1/nodes/hard-accrual-legend-type/body ("here from our partner firm" → type E4)
/v1/nodes/hard-accrual-legend-tenure/body ("been here eight months" → tenure T1)
/v1/nodes/hard-accrual-legend-site/body ("fully from home" → site L4)
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body (1.42 days/month, 7-day carry-over limit)

4. Notes
All three qualifiers in the question ("here from our partner firm", "been here eight months", "fully from home") matched their legend rows exactly, word for word — no nearest-entry judgment call was needed, which is unusual and worth flagging since the legends explicitly warn that a mismatch requires picking the nearest entry and recording the choice. The one place this could have gone wrong is the version check: there are three superseded/current versions of the accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns bluntly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls after the 2026-01-01 cutover, so the current table (`sec-hard-accrual`) is correct here, but it would have been an easy mistake to skip that check and assume "current" without verifying the date against the cutover. Also worth noting: I read "how much can I still be holding in January" as asking for the carry-over limit (the cap on days held into the new year), not a projection of accrued-but-unused balance, since no starting balance or usage history was given or available through this row.
