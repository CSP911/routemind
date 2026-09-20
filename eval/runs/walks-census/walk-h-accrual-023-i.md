1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. Answer
Accrues 0.62 days per month. Can hold (carry-over limit) up to 13 days into January.
(Type E1 = regular payroll, tenure T3 = five years' service, site L4 = fully from home, under the current accrual table in force since 2026-01-01.)

3. Source
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body

4. Notes
- There are three superseded/current versions of the accrual table (leave-accrual, hard-accrual-v2, sec-hard-accrual), each indexed differently (one, two, then three qualifiers). It would have been easy to grab an old table by habit; checked hard-accrual-legend-revision explicitly and confirmed today's date (2026-09-20) falls under the current table (sec-hard-accrual, in force from 2026-01-01 onward, no end date), so it also governs carry-over into January 2027.
- All three qualifiers ("regular payroll", "five years", "fully from home") happened to map to exact legend entries (E1, T3, L4) with no need to round to a nearest band — a case where the "nearest entry" fallback note in each legend wasn't needed, but it's easy to miss that the legends are the *only* place holding the type/tenure/site → code mapping, and skipping straight to the row grid without them would have made the address unguessable (addresses aren't meant to be constructed).
- "How much can I still be holding in January" reads as the carry-over limit (13 days), not the monthly accrual — the row's "Carry-over limit, days" field answers it directly, so no separate lookup was needed for that half of the question.
