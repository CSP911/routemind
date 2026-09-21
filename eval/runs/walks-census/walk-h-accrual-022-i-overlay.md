## Commands

./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Singapore, regular payroll, 5 years tenure: monthly leave accrual rate and max carry-over/holding cap in January" --member /v1/regions/attendance "leave accrual and carry-over rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_c1f5c0 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body

## Answer

Accrues 0.60 days per month. Can hold (carry-over limit) up to 12 days into January.

## Source

- /v1/nodes/hard-accrual-legend-revision/body (confirms 2026-01-01-onward table is the correct version for today, 2026-09-20)
- /v1/nodes/hard-accrual-legend-type/body ("on the regular payroll" → type E1)
- /v1/nodes/hard-accrual-legend-tenure/body ("been here five years" → tenure T3)
- /v1/nodes/hard-accrual-legend-site/body ("in the Singapore entity" → site L3)
- /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body (0.60 days/month accrual, 12-day carry-over limit)

## Notes

The accrual subject has three superseded/current versions covering different date ranges, flagged loudly by hard-accrual-legend-revision — worth checking explicitly since the oldest version doesn't say it was replaced. Today's date (2026-09-20) falls in the 2026-01-01-onward range, so sec-hard-accrual is correct; a naive approach could have missed the version check and still landed on the right table by luck, but it wasn't obvious until reading the legend page.

The three qualifiers (type/tenure/site) are each a small vocabulary translation exercise — the row addresses are built from codes (e1/t3/l3), not from the user's own words, and the legends explicitly warn "never build one," so I read each legend rather than guessing the coding scheme from the address list. "Regular payroll" mapping to "E1" and Singapore mapping to "L3" (third in a list that's otherwise Seoul/Busan-centric) were the least obvious of the three.

"How much can I still be holding in January" reads naturally as the carry-over limit (12 days) — the cap on what can be held over into the new year — rather than a literal balance calculation, since the KB has no data on the person's actual leave usage/balance, only the policy limits.
