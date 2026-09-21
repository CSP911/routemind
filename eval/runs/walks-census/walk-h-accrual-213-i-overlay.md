1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 2 years tenure, fully remote: monthly leave accrual and max carryover holdable in January?" --member /v1/regions/attendance "leave accrual, part-time/reduced-schedule proration, and carryover rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_bc230e --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body

2. **Answer**
Accrues 1.18 days per month. Carry-over limit is 10 days — that is the maximum you can still be holding into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirms the 2026-01-01-onward table is the correct version for today's date, 2026-09-21)
/v1/nodes/hard-accrual-legend-type/body ("in three days a week" → type E3)
/v1/nodes/hard-accrual-legend-tenure/body ("been here two years" → tenure T2)
/v1/nodes/hard-accrual-legend-site/body ("fully from home" → site L4)
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body (the answer: 1.18 days/month accrual, 10-day carry-over limit)

4. **Notes**
This walk was unusually clean — all three qualifiers in the question ("three days a week," "two years," "fully from home") matched a legend row's left-hand phrasing verbatim, so there was no fuzzy judgment call on which code to pick. The one place I could have gone wrong is the accrual-version trap: `sec-hard-accrual` is explicitly flagged as superseding two older versions (`hard-accrual-v2` for 2024-07-01–2025-12-31, and the original `leave-accrual` before that), and the legend-revision page warns that reaching for the newest table is wrong for a question dated before 2026-01-01. Since today is 2026-09-21, the current table is correct, but I checked the revision page explicitly rather than assuming — it's clearly built to catch that mistake. I read "how much can I still be holding in January" as asking for the carry-over limit (10 days), not a computed balance, since RouteMind has no record of the person's actual leave usage/balance to compute from — the table only states the policy ceiling.
