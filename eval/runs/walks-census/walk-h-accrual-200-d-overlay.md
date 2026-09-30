1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E3, tenure T1, site L1: monthly accrual rate and max carryover/cap holdable in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site, in force from 2026-01-01"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_05d086 --outcome answered --used /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body

2. **Answer**: You accrue 1.04 days per month. You can hold (carry over) at most 4 days.

3. **Source**: /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body

4. **Notes**: The attendance area table lists three accrual versions (a legacy `leave-accrual`, a superseded `hard-accrual-v2` for 2024-07-01 to 2025-12-31, and the current `sec-hard-accrual` in force from 2026-01-01) — easy to grab the wrong one if you don't notice the "SUPERSEDED" / "CURRENT" markers in the table row descriptions. I went straight for the current table since today's date (2026-09-20/21) falls in its effective range. The overlay member I registered was the parent table (`sec-hard-accrual`), not the specific E3/T1/L1 row, since the row address only became visible after opening that table — the close command flagged the row as "reached" rather than a named member, which is just bookkeeping, not an error. "How much can I still be holding in January" reads ambiguously (does it mean the balance at a fixed calendar point, or the carry-over cap?) but the row's "Carry-over limit, days: 4" is the only figure in the document answering a holding/retention question, so that's what's reported.
