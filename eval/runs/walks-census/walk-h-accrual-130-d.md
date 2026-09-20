1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l1/body

2. **Answer**
For type E2, tenure T4, site L1 (current table, in force since 2026-01-01): accrues 0.96 days per month. The carry-over limit is 13 days — that is the most you can still be holding into January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l1/body

4. **Notes**
There are three versions of the leave accrual page (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision file warns that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so that was the correct one to use — but this was the one place it would have been easy to grab the wrong version without checking the warning page first. The question already gave the type/tenure/site codes (E2, T4, L1) directly, so no legend lookup (site/tenure/type legend files) was needed to translate plain-language qualifiers into codes. "How much can I still be holding in January" was read as the row's "Carry-over limit" field (13 days) — the table has no separate January-specific figure, and this is the only field describing a balance that persists into the new year.
