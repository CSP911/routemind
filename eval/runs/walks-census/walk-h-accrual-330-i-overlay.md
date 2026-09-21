1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 9 years tenure, Seoul office: monthly leave accrual rate and max carryover holdable in January" --member /v1/regions/attendance "leave accrual, tenure-based leave, carryover rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b17f28 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body
```

2. **Answer**
Accrues 1.60 days per month. Carry-over limit is 13 days — that is the most that can still be held (e.g. going into January).

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (established today's date, 2026-09-21, selects the current table, not the superseded `hard-accrual-v2`)
- /v1/nodes/hard-accrual-legend-type/body ("here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body ("been here nine years" → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body ("at the Seoul office" → site L1)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l1/body (the answer: 1.60 days/month accrual, 13-day carry-over limit)

4. **Notes**
- Leave accrual has three versions in force over different date ranges, and the legend-revision page warns explicitly that the oldest version says nothing about being superseded — reaching for the newest table without checking the date would be wrong for a 2025-dated question. Today's date (2026-09-21) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct here, but this is the kind of question where I'd have silently gotten it wrong for a slightly different date.
- The employment-type legend's phrasing "here from our partner firm" is a verbatim match to the question's own phrasing, which made E4 unambiguous — no interpretation needed.
- Tenure legend has exact bands (8 months, 2 years, 5 years, 9 years) rather than ranges, and "nine years" landed on an exact value (T4) rather than needing the "nearest entry" fallback the legend mentions for off-list values.
- The question's second half ("how much can I still be holding in January") is really asking about the carry-over limit, not a January-specific accrual figure — there is no separate January rule in this row; the 13-day carry-over limit is the ceiling on what can be held at any point, including into January.
