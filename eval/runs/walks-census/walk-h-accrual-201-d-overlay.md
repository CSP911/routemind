1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T1, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carry-over cap by employee type/tenure/site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e30143 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body

2. **Answer**:
Accrues 1.06 days per month. Carry-over limit (the most you can still be holding into January) is 5 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l2/body

4. **Notes**:
Leave accrual has three superseded versions keyed to different date ranges, and the legend-revision doc warns that reaching for the newest table is wrong for any question dated before 2026-01-01 — the oldest version doesn't even say it was replaced, so guessing wrong is easy. Today's date (2026-09-20/21) and the question's three qualifiers (type/tenure/site) both point to the current table `sec-hard-accrual`, in force from 2026-01-01, so that was a safe pick, but it's the kind of thing that could go wrong silently on a differently-dated question. Once at the table, E3/T1/L2 was an exact, unambiguous row — no legend translation needed since the question already used the table's own codes. The "how much can I still be holding" phrase maps to "carry-over limit" in the row, not the monthly accrual figure — easy to conflate the two numbers if skimming.
