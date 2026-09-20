1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body

2. **Answer**
For type E3, tenure T4, site L2: accrues 1.30 days per month. Carry-over limit (the most you can still be holding into January) is 14 days.

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body
(also consulted for date-versioning context: /v1/nodes/hard-accrual-legend-revision/body)

4. **Notes**
The attendance area lists three versions of the accrual rules (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), with a warning that the oldest page never says it was superseded — reaching for the newest by reflex would have been wrong for a 2025-dated question. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so that was the correct version to use; no ambiguity here since the question gave no date of its own to check against.

The question already supplied the type/tenure/site codes (E3, T4, L2) directly, so there was no need to open the legend files (site/tenure/type) to translate plain-language qualifiers into codes — the row address could be built straight from the table listing.

The only real interpretive step was mapping "how much can I still be holding in January" to the row's "Carry-over limit" field — the table doesn't use the word "January" anywhere, but a carry-over limit is by definition the cap on balance held across the year boundary into the new year, so this reading seems solid.
