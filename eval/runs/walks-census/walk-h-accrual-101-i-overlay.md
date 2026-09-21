1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Two-year contract employee, 8 months tenure, Busan branch: monthly leave accrual rate, and max balance holdable in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site - likely has the monthly accrual rate for a contract employee at Busan"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_612f9a --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body

2. **Answer**:
Accrues 0.74 days per month. Carry-over limit is 5 days — that is the most you can still be holding once the year turns over into January.
(Two-year contract → type E2; eight months' service → tenure T1; Busan branch → site L2. Row E2/T1/L2, in force since 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-accrual-legend-type/body (maps "two-year contract" to type E2)
- /v1/nodes/hard-accrual-legend-tenure/body (maps "eight months" to tenure T1)
- /v1/nodes/hard-accrual-legend-site/body (maps "Busan branch" to site L2)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l2/body (the accrual and carry-over figures)

4. **Notes**:
The three qualifiers in the question (contract type, tenure, site) each had to be translated through a separate legend document before the actual row address could be built — the accrual table itself never explains what "E2", "T1", "L2" mean, only the legends do. It would be easy to guess wrong here, e.g. assume "eight months" rounds up toward T2 ("two years") rather than down to T1; the legend is explicit that you take the tenure band you have already reached, not the one you're heading toward, so eight months stays T1.

The overlay table under /v1/nodes/sec-hard-accrual listed all 64 type/tenure/site row combinations plus the three legends as candidate rows — the legends were not something I thought to add as explicit overlay members before reading them, so `overlay close` reported them as "reached" (used but never named as members) rather than as tracked/removed members. Functionally it didn't affect the answer, but if the overlay's membership list is itself scored, note that the legends should probably have been added explicitly via `overlay add` before reading them.

The question's phrase "how much can I still be holding in January" is ambiguous between "the carry-over cap" and "projected balance after 8 months of accrual." I read it as the cap (5 days), since the row's own field is literally named "Carry-over limit, days" and January is when a carry-over would apply — but a literal month-by-month balance projection was not attempted, since the table gives a flat monthly rate rather than a schedule, and the question doesn't specify a starting balance or whether any leave has already been taken.
