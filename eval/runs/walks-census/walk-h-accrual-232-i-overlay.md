1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 9 years tenure, Singapore entity: monthly leave accrual rate and max carry-forward cap into January" --member /v1/regions/attendance "attendance table covers leave accrual, part-time proration, tenure-based accrual, and carry-forward caps"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f0c223 --outcome answered --used /v1/regions/attendance /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body

2. **Answer**: You accrue 1.32 days of leave per month. The carry-over limit into January is 15 days.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirms which of the three accrual versions applies for today's date)
- /v1/nodes/sec-hard-accrual (the current accrual table, in force from 2026-01-01)
- /v1/nodes/hard-accrual-legend-type/body (maps "in three days a week" → type E3)
- /v1/nodes/hard-accrual-legend-tenure/body (maps "been here nine years" → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body (maps "in the Singapore entity" → site L3)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body (the row with the figures: 1.32 days/month accrual, 15-day carry-over limit)

4. **Notes**: The accrual subject has three superseded/current versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each covering a different date range, and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20/21) falls under the current table, so this wasn't a trap here, but it would have been easy to skip that check and just grab the first accrual-looking table. The three qualifiers (type/tenure/site) are each defined in a separate legend file rather than in the row table itself, and the legends explicitly warn to use the nearest lower band if an exact match isn't listed — "three days a week" and "nine years" happened to match exactly (E3, T4), so no judgment call was needed there. "How much can I still be holding in January" maps to the row's "carry-over limit" field — the wording doesn't use the word "carry-over," so it would be easy to misread it as asking about the monthly accrual figure alone.