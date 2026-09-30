1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 8 months tenure, fully remote/work-from-home: monthly leave accrual rate and max carryover/holding into January?" --member /v1/regions/attendance "leave accrual rates, carryover rules, and how partner-firm/remote employment type affects it"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_243677 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body

2. **Answer**:
Accrues 1.42 days per month. Maximum you can be holding (carry-over limit) is 7 days — so that is the most you can still be holding when January comes around. (Note: this row also states leave does not accrue during unpaid leave, and 5 working days' notice is required to book leave, in case those are relevant follow-ups.)

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirms current table applies — today, 2026-09-20/21, falls in the "2026-01-01 onwards" version, so no older version applies to either the current month or January)
- /v1/nodes/hard-accrual-legend-type/body (maps "here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body (maps "been here eight months" → tenure T1)
- /v1/nodes/hard-accrual-legend-site/body (maps "fully from home" → site L4)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l4/body (the row with the actual figures: 1.42 days/month accrual, 7-day carry-over limit)

4. **Notes**:
The three legend phrases in the question — "here from our partner firm," "been here eight months," and "fully from home" — turned out to be the exact literal wording used in the legend tables' left-hand column, not paraphrases needing interpretation. That made picking E4/T1/L4 unambiguous, but it was worth double-checking each legend rather than guessing the codes from the words alone, since the legends explicitly warn "if what you have is not listed, take the nearest entry" — implying an exact match isn't guaranteed and shouldn't be assumed.

The trickiest part was the date/version check. There are three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges, and the legend-revision doc warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20 per the task, 2026-09-21 per a later system reminder) falls after 2026-01-01, and the question's forward-looking part ("how much can I still be holding in January") also falls after that date, so the current table (`sec-hard-accrual`) is correct for both halves of the question — no version-straddling issue here, but it would have been easy to skip the legend-revision check entirely and get lucky, or to wrongly assume the older `hard-accrual-v2` applied given the "eight months" tenure detail (tenure has nothing to do with which version's document to use — that was a possible false association to avoid).
