1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T2, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual and carry-over cap questions live in attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f54f41 --outcome answered --used /v1/regions/attendance /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body

2. **Answer**: For type E1, tenure T2, site L3 (under the current accrual table, in force from 2026-01-01): accrues 0.52 days per month; carry-over limit (the most that can still be held/carried into January) is 9 days.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date, 2026-09-20 — the current one)
- /v1/nodes/sec-hard-accrual (the current accrual table, listing the row addresses by type/tenure/site)
- /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body (the actual figures used in the answer)

4. **Notes**: The question's E1/T2/L3 codes matched the row-address naming convention directly, so I didn't need to open the site/tenure/type legend files to translate plain-language qualifiers into codes — worth double-checking in other walks where the question gives descriptions instead of codes. The one place this could have gone wrong is the three-version trap flagged by `hard-accrual-legend-revision`: there are three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges, and grabbing the newest-looking one without checking the date would have been the easy mistake for a question dated in 2025. Since today is 2026-09-20, the current table (`sec-hard-accrual`, in force from 2026-01-01) is correct here, but I read the revision-legend explicitly before trusting that. The "carry-over limit, days: 9" field is what I'm reading as "how much can I still be holding in January" — the row doesn't use the word "January" itself, so this is an interpretation (carry-over cap = the ceiling on balance held into the new year) rather than a verbatim match; flagging in case the intended reading differs.
