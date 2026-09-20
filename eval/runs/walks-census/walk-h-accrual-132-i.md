1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body

2. **Answer**
Accrues 1.00 day per month. Carry-over limit (the most you can be holding going into January) is 15 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body

4. **Notes**
Leave accrual has three superseded versions keyed by date (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`); the legend-revision page warns explicitly not to reach for the newest by default. Today's date (2026-09-20) falls after the 2026-01-01 cutoff, so the current table (`sec-hard-accrual`) is correct here, but this is exactly the kind of question where grabbing the current table without checking the date would sometimes be wrong — worth flagging since the question itself doesn't mention a date.

The three qualifiers (type/tenure/site) are each resolved by a separate legend, and each legend is explicit that its mapping is the *only* place the translation is written — the row addresses themselves give no hint which plain-language description maps to which code. "Two-year contract" mapped cleanly to type E2, "nine years" to tenure T4, and "Singapore entity" to site L3, all exact matches with no need to fall back to "nearest entry" behavior. Easy to construct a wrong address here by guessing rather than reading all three legends first.

The question asks two things — monthly accrual rate and how much can still be held in January — and both are answered by the same row: "Accrues per month, days" (1.00) and "Carry-over limit, days" (15). I read "how much can I still be holding in January" as asking for the carry-over cap rather than a specific projected balance, since no starting balance or booking history was given or available through this tool.
