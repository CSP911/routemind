1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l3/body

2. **Answer**
Accrues 1.08 days per month. Carry-over limit is 6 days — that is the maximum that can still be held into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l3/body

4. **Notes**
Leave accrual has three superseded versions with different dates; the legend-revision page warns not to reach for the newest by reflex. Today (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct here — but this is exactly the kind of question where grabbing the current table without checking dates would happen to be right for the wrong reason. For a question dated in 2025 the answer would have been the superseded `hard-accrual-v2` instead.

The three qualifiers ("three days a week" → type E3, "eight months" → tenure T1, "Singapore entity" → site L3) are each easy to fumble: "three days a week" sounds like it could describe hours/scheduling rather than an employment-type code, and "Singapore entity" isn't an obvious match for "site" until reading the site legend, which maps it to L3 specifically (distinct from Seoul/Busan offices or remote). Each legend explicitly warns it is the only place its mapping is written and not to assume a nearest match without recording it — none of the three needed a nearest-match fallback here, all three had exact hits.

The question's "how much can I still be holding in January" is answered by the row's carry-over limit, not the monthly accrual figure — the row only exposes one carry-over number, not a January-specific one, so I read it as the standing cap and reported it as such.
