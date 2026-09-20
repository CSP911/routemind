1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body

2. **Answer**
You accrue 1.62 days per month. The carry-over limit is 14 days — that is the most you can still be holding when January comes around (unapproved excess above that is settled at 14 days and the difference is not recoverable; an unavoidable excess can be claimed separately with a written statement, decided by the budget holder).

3. **Source**
/v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l2/body

4. **Notes**
The main risk here was version confusion: the attendance table lists three separate accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with overlapping subject matter and no indication on the oldest one that it was ever superseded. The legend-revision page was the thing that resolved this — since today's date (2026-09-20) falls after 2026-01-01, the current table `sec-hard-accrual` is the correct one, not the v2 or oldest page. It would have been easy to grab the wrong version if I'd skipped that check. Once on the current table, the row was addressed directly by the three qualifiers (E4, T4, L2) with no ambiguity, and it stated both figures (monthly accrual and carry-over limit) in one place, so no legend lookups were needed. I read "how much can I still be holding in January" as asking for the carry-over limit, which is the figure the table itself frames as governing what happens with an excess/holdover — this is the most natural reading of that document.
