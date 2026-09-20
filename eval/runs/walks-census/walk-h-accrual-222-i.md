1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body

2. **Answer**
Accrues 1.24 days per month. Carry-over limit (the most that can still be held going into January) is 12 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body

4. **Notes**
The attendance table lists three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no obvious warning at that level that they conflict — reaching for whichever looked newest would have been a guess. The legend-revision doc makes clear today's date (2026-09-20) falls in the "2026-01-01 onwards" band, so `sec-hard-accrual` is the right table; the two older versions were skipped deliberately, not overlooked.

The three qualifiers (type/tenure/site) are each resolved by a separate legend file, and each legend explicitly says "if what you have is not listed, take the nearest entry below/above" — none of that fuzziness was needed here since "three days a week," "five years," and "Singapore entity" match legend rows exactly (E3, T3, L3).

The "how much can I still be holding in January" phrasing initially read like it might need a separate carry-forward/rollover policy page (something distinct from the accrual table), but the row itself already states a "Carry-over limit, days" field, which is exactly what caps balance held into the new year — no second document was needed or found for that figure.
