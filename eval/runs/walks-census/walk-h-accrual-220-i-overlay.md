1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 5 years tenure, Seoul office: monthly leave accrual rate and max carryover/balance holdable in January?" --member /v1/regions/attendance "attendance covers leave accrual, balances, carryover, part-time/pro-rated leave"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py overlay close --id ov_2026-09-20_ad0422 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**
Accrues 1.20 days per month. Carry-over limit is 10 days — that is the most that can still be held (carried into January).

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l1/body

4. **Notes**
The three qualifiers in the question ("three days a week", "five years", "Seoul office") map to codes only through three separate legend files (hard-accrual-legend-type/tenure/site) — none of this is guessable, and the row address itself (hard-accrual-row-type-e3-tenure-t3-site-l1) has to be built from those three lookups rather than found by browsing. "Three days a week" maps to type E3, which is easy to misread as a schedule/remote-work detail rather than an employment-type classification — the legend explicitly reserves it for that, and the accrual/carry-over figures differ across E1–E4, so getting this wrong would silently pick the wrong row.

The bigger trap was the revision history: hard-accrual-legend-revision warns that this subject has been rewritten three times and that reaching for the newest version is wrong for any question dated before 2026-01-01. The question doesn't give an explicit date, but "how much can I still be holding in January" clearly asks about a future/ongoing state relative to today (2026-09-20), so the current table (sec-hard-accrual, in force 2026-01-01 onward, no end date) is the right one — I checked the revision file specifically to rule out picking the superseded hard-accrual-v2 by mistake.

"How much can I still be holding in January" reads at first like it could be about the annual entitlement/balance rather than a carry-over cap. I briefly considered the older annual-leave → leave-accrual table but that document is the superseded (pre-2024-07-01) version, not part of the current accrual scheme, so I did not use it. The row's own "Carry-over limit, days" field is the direct answer to that half of the question.
