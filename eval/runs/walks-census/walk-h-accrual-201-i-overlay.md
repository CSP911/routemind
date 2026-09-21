1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Part-time (3 days/week) employee, 8 months tenure, Busan branch: monthly leave accrual rate and max holdable/carryover balance in January?" --member /v1/regions/attendance "leave accrual, part-time proration, and carryover cap questions live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a96073 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body
```

2. **Answer**
Accrues 1.06 days per month. The carry-over limit (the most that can still be held / carried into January) is 5 days.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirmed the current table, not the superseded versions, applies for a question dated 2026-09-20)
- /v1/nodes/hard-accrual-legend-type/body ("in three days a week" → type E3)
- /v1/nodes/hard-accrual-legend-tenure/body ("been here eight months" → tenure T1)
- /v1/nodes/hard-accrual-legend-site/body ("at the Busan branch" → site L2)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body (the row with the actual figures: 1.06 days/month accrual, 5-day carry-over limit)

4. **Notes**
Leave accrual has three superseded versions indexed differently, and the legend-revision doc warns the oldest version doesn't announce that it's been replaced — so I checked the revision page first before trusting `sec-hard-accrual` as current for today's date (2026-09-20 falls after 2026-01-01, so the current table is correct). The three qualifiers in the question ("three days a week", "eight months", "Busan branch") each mapped cleanly and exactly to one legend row each (E3/T1/L2) with no ambiguity or nearest-match judgment needed. The row itself answers both halves of the question directly — "accrues per month" and "carry-over limit" — so no second row or cross-reference was needed. One point worth flagging: "how much can I still be holding in January" reads naturally as asking about a carryover cap tied to year-end/January, and the row's "Carry-over limit" field is the only figure in the document that matches that shape, but the row doesn't explicitly say "January" — I'm inferring that carry-over limit is what caps the balance going into the new year. That inference seems safe given the document structure, but it's the one place the wording didn't line up one-to-one.
