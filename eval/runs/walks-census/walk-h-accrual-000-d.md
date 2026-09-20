1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/hard-accrual-legend-revision
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body

2. **Answer**
For type E1, tenure T1, site L1: accrues 0.40 days per month. The carry-over limit is 4 days — the most you can still be holding in January (i.e., carried over the year boundary).

3. **Source**
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l1/body

4. **Notes**
Leave accrual has three superseded versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend-revision warning explicitly said reaching for the newest is wrong for anything dated before 2026-01-01. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so that was the correct row — but this was a real branch point, not a formality, since the middle version would have been the right answer for any 2025-dated question. The question's "how much can I still be holding in January" phrasing isn't a separate figure in the table — it maps directly to "Carry-over limit, days," which is the balance you're allowed to still be holding when the year rolls over. No ambiguity once the row was found; the type/tenure/site codes E1/T1/L1 were given directly in the question and matched a row verbatim, so no legend lookup was needed to translate qualifiers.
