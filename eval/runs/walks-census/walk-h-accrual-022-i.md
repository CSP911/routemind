1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body

2. **Answer**
Accrues 0.60 days per month. Carry-over limit (the most you can still be holding when the year turns over into January) is 12 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirms today, 2026-09-20, falls under the current 2026-01-01 version, not the two superseded ones)
/v1/nodes/hard-accrual-legend-type/body (regular payroll → type E1)
/v1/nodes/hard-accrual-legend-tenure/body (five years → tenure T3)
/v1/nodes/hard-accrual-legend-site/body (Singapore entity → site L3)
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body (0.60 days/month accrual, 12-day carry-over limit)

4. **Notes**
The legend-revision page is the thing worth flagging: it warns that leave accrual has three separately-written versions (pre-2024-07-01, 2024-07-01–2025-12-31, and current from 2026-01-01) and that "the oldest says nothing at all about having been replaced," so reaching for the newest table without checking the date is explicitly called out as a mistake. Today's date (2026-09-20) puts this squarely in the current `sec-hard-accrual` table, so no version ambiguity here — but it's the kind of question where an unwary walk would grab the wrong era.
The three qualifiers (type/tenure/site) each had a dedicated legend page and each said "this table is the only place the mapping is written down" — five years mapped exactly onto tenure T3 with no rounding needed, so no ambiguity there either. "How much can I still be holding in January" isn't phrased in the source as a calendar-year carryover statement, but "carry-over limit" is the only figure on the row that answers a "how much can I still be holding" question, so I read the two as the same thing.
