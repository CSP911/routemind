1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body

2. **Answer**
For type E2, tenure T3, site L2 (current table, in force since 2026-01-01):
- Accrues 0.90 days per month.
- Carry-over limit is 11 days — that is the most you can still be holding going into January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body

4. **Notes**
The question already gave the codes (E2, T3, L2) exactly as the row is named, so no legend lookup
was needed to translate a plain-language description into type/tenure/site codes — that saved a
step but is also where I'd have gone wrong if the codes hadn't matched a real row.

The attendance area's table flagged that leave accrual has THREE versions with different figures
(a legend-revision warning), and the accrual table itself is explicit that it's the version "in
force from 2026-01-01," replacing `hard-accrual-v2` (2024-07-01 to 2025-12-31) and `leave-accrual`
before that. Today is 2026-09-20, so the current table is the right one — but this is exactly the
kind of walk where picking an older, similarly-named row (there are `hard-accrual-v2` rows too)
would silently give a wrong, superseded number. I stayed on the current table and didn't open the
older versions.

The phrase "how much can I still be holding in January" maps to the row's "Carry-over limit, days"
field — I read this as the cap on the balance you're allowed to carry over into the new year. The
row doesn't give a separate, January-specific figure or deadline, so I'm reporting the carry-over
limit itself as the answer to that half of the question; if the asker meant something more specific
(e.g., a deadline by which carried-over days must be used), that wasn't present in this document.
