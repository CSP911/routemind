1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py read /v1/nodes/annual-leave/body

2. **Answer**: For type E3, tenure T4, site L4 (current table, in force since 2026-01-01, which applies to today's date 2026-09-20): accrues 1.34 days per month. Carry-over limit is 16 days — that is the most you can still be holding into January.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body (the figures: 1.34 days/month accrual, 16-day carry-over limit)

4. **Notes**: The three-version warning page made it clear the current table (sec-hard-accrual, since 2026-01-01) is the right one for a 2026-09-20 question, not the superseded hard-accrual-v2 or the oldest leave-accrual — worth checking explicitly rather than assuming "newest is always right," since the same warning page says that assumption breaks for 2025-dated questions.

The near-miss: I also opened /v1/nodes/annual-leave/body out of general-context curiosity, and it flatly states "Unused days do not roll over" — "they lapse." That directly contradicts the 16-day carry-over limit in the row I'd just read, and if read first (or read as authoritative) it would have produced a wrong "0 days carry over" answer. That annual-leave page turns out to describe the oldest, one-qualifier entitlement scheme (length-of-service only, no type/tenure/site), which is superseded for anyone whose leave is governed by a type/tenure/site row like this one. Since the question gives explicit E3/T4/L4 codes, only the current three-qualifier table applies, and its own carry-over limit field is the answer — the older page's "no rollover" language should not be read as a general rule that overrides it.
