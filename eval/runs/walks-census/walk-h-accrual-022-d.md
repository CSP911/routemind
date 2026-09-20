1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**: For type E1, tenure T3, site L3 (current table, in force from 2026-01-01): you accrue 0.60 days per month. The carry-over limit is 12 days — that is the most you can still be holding going into January (the new year).

3. **Source**:
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l3/body
/v1/nodes/hard-accrual-legend-revision/body

4. **Notes**: The area listing under /v1/regions/attendance shows a loud warning file, `hard-accrual-legend-revision`, saying leave accrual has three versions with different dates in force, and that reaching for the newest is wrong for anything before 2026-01-01. Since today is 2026-09-20 and the question carries no other date, the current table (`sec-hard-accrual`, in force from 2026-01-01) is the right one — but this is exactly the trap the revision page is warning about, and I checked it explicitly rather than assuming "current" was safe by default. The three-qualifier row address (type/tenure/site) made the exact match unambiguous once inside `sec-hard-accrual`, so no legend lookups for the type/tenure/site codes were needed since the user already gave codes (E1/T3/L3) rather than plain-language descriptions. The phrase "how much can I still be holding in January" is not spelled out anywhere as a January-specific rule — I read it as asking for the carry-over limit (12 days), since that is the field in the row governing what balance survives into the new year; there was no separate January-specific cap elsewhere in this row to contradict that reading.
