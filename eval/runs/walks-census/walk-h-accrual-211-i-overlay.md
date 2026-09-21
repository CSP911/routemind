1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 2 years tenure, Busan branch: monthly leave accrual and max carryover into January" --member /v1/regions/attendance "leave accrual, part-time proration, and carryover rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_909faf --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body

2. **Answer**: Accrues 1.14 days per month. Carry-over limit is 8 days — that is the most that can still be held into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body

4. **Notes**: The leave accrual subject has three superseded versions covering different date ranges, and the legend-revision doc warns that reaching for the newest version is wrong for anything before 2026-01-01, and that the oldest version says nothing about being replaced. Today's date (2026-09-20/21) falls inside the current version's window (2026-01-01 onward), so `sec-hard-accrual` was correct — but this was the one place a careless walk would go straight to the newest table without checking, and would happen to still be right here, though it would be wrong for a question dated in 2025. The three qualifiers in the question ("three days a week", "two years", "Busan branch") mapped cleanly and exactly onto the legend entries for type (E3), tenure (T2), and site (L2) with no fuzzy nearest-entry judgment calls needed, which made this walk unusually clean once the correct table version was identified. The row itself answers both halves of the question directly: the monthly accrual figure and the carry-over limit, which is the ceiling on what can still be held into January.
