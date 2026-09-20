1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l1/body

2. **Answer**
For type E4, tenure T2, site L1 (current table, in force since 2026-01-01): accrues 1.44 days per month. Carry-over limit is 7 days — that is the maximum you can still be holding, e.g. in January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l1/body

4. **Notes**
The attendance region lists three versions of the leave-accrual subject (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), with an explicit warning that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force from 2026-01-01), so no correction was needed here, but it would have been an easy trap if the question had been dated in 2025. The E4/T2/L1 row was addressed directly by the codes given in the question, so the legend files for type/tenure/site were not needed — worth flagging in case those codes were meant to be interpreted rather than taken literally, but the row existed exactly as named. "How much can I still be holding in January" reads naturally as the carry-over limit field, which the row itself frames as a hard cap (with a separate note on what happens if it's exceeded), so I treated that as the answer rather than looking for a separate "January" rule elsewhere.
