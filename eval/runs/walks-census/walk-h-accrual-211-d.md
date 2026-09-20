1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body

2. **Answer**
For type E3, tenure T2, site L2 (current table, in force since 2026-01-01): you accrue 1.14 days of leave per month, and the carry-over limit is 8 days — that is the most you can still be holding once the year rolls over into January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l2/body

4. **Notes**
The attendance table lists three versions of the accrual rules (a legend-revision file plus a superseded `hard-accrual-v2`), and it would have been easy to grab the wrong-dated table. Since today is 2026-09-20 and the row itself states it has been in force from 2026-01-01 with no end date, `sec-hard-accrual` is the current one and no cross-check against the older versions was needed. The question gave the type/tenure/site codes directly (E3, T2, L2), so the legend files for translating plain-language qualifiers into those codes weren't needed either. The only mild ambiguity was "how much can I still be holding in January" — read as asking about the carry-over limit (8 days), since that's the figure that caps what survives into the new year.
