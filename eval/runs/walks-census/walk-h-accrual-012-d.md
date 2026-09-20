1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body

2. **Answer**
For type E1, tenure T2, site L3 (current table, in force since 2026-01-01): accrues 0.52 days per month, with a carry-over limit of 9 days — that's the most you can still be holding in January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body

4. **Notes**
The attendance area lists three versions of the accrual table (`leave-accrual`, `hard-accrual-v2`, and the current `sec-hard-accrual`), flagged by a legend-revision warning — easy to grab a superseded row by mistake. Today's date (2026-09-20) falls inside the current table's "in force from 2026-01-01" window, so `sec-hard-accrual` was the right one; the row itself also restates this version boundary, which confirmed it. The question gave the type/tenure/site codes directly (E1/T2/L3), so no legend lookup was needed to translate a plain-language description into codes — the 64-row index just needed a direct match on address name. The "how much can I still be holding in January" phrasing isn't self-evidently about carry-over — I read it as asking for the carry-over limit (the balance cap you can hold going into the new year), since that's the only figure in the row that speaks to a limit on holdings rather than a rate.
