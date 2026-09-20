1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l3/body

2. **Answer**
Accrues 0.44 days per month. Carry-over limit into January is 6 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l3/body

4. **Notes**
Leave accrual has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns the oldest version doesn't admit it's been replaced — easy to grab the wrong one if you don't check dates first. Today (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-accrual` is correct; no ambiguity here since the date isn't in the 2025 window the warning calls out as the tricky case.

The three qualifiers (employment type, tenure, site) mapped cleanly and exactly: "regular payroll" → E1, "eight months" → T1 (listed verbatim in the tenure legend), "Singapore entity" → L3 (also verbatim). No nearest-match guessing was needed, which is itself worth flagging since the legends explicitly allow for fuzzy matching when the input isn't listed — this walk didn't require it.

The only interpretive judgment call: "how much can still be holding in January" was read as the year-end carry-over limit (6 days), since that's the only figure in the row about how much leave can persist across the year boundary. The row itself doesn't use the word "January," so this mapping relies on inference from context (carry-over limits apply at year-end, into the new year).
