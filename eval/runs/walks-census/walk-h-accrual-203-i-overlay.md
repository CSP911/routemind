1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Part-time (3 days/week), 8 months tenure, fully remote: monthly leave accrual rate and max carryover balance into January?" --member /v1/regions/attendance "leave accrual, part-time proration, and carryover rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9cd4cc --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l4/body

2. **Answer**
Accrues 1.10 days of leave per month. The carry-over limit is 7 days — that is the most that can still be held once January (the new accrual year) starts; anything approved and exceeding that is a separate case decided by the budget holder, and anything unapproved in excess is forfeited.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirms today's date, 2026-09-20/21, falls under the current 2026-01-01-onward table, not the superseded versions)
/v1/nodes/hard-accrual-legend-type/body ("in three days a week" → type E3)
/v1/nodes/hard-accrual-legend-tenure/body ("been here eight months" → tenure T1)
/v1/nodes/hard-accrual-legend-site/body ("fully from home" → site L4)
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l4/body (the row itself: 1.10 days/month accrual, 7-day carry-over limit)

4. **Notes**
The accrual table is indexed by three codes (type, tenure, site) and none of the three legends repeat the plain-language phrasing in the question verbatim — the question's own wording ("three days a week", "eight months", "fully from home") happens to match the legend rows almost exactly, which made mapping straightforward here, but it would be easy to rush this and guess a row address instead of reading each legend. I deliberately read all three legends before picking a row rather than assuming the obvious mapping (e.g. "eight months" is close to but not the same as "two years" — T1 vs T2 — so skipping the tenure legend could plausibly cost a wrong tenure band on a less clean phrasing).
The bigger trap was versioning: `sec-hard-accrual` is explicitly marked as replacing two older tables (`hard-accrual-v2` for 2024-07-01–2025-12-31, and `leave-accrual` for before that), and the legend-revision page warns the oldest table "says nothing at all about having been replaced." Today's date (2026-09-20/21) is safely inside the current table's range, so no ambiguity in this case, but a question dated in 2025 would need `hard-accrual-v2` instead, and grabbing the newest table by reflex would have been wrong.
"How much can I still be holding in January" reads as asking about carryover into the new year — I took this as the row's "Carry-over limit, days" field (7) rather than the monthly accrual figure, since the row explicitly separates the two and the carry-over limit is the value with an actual cap tied to crossing into a new period.
