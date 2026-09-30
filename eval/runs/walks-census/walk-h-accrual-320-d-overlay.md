1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E4, tenure T3, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/nodes/sec-hard-accrual "current accrual table by type, tenure, site since 2026-01-01" --member /v1/nodes/annual-leave "entitlement and booking, may cover carryover/holding cap" --member /v1/nodes/sec-days-that-decide-money "key days affecting allowances/payouts, may relate to January cap"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_54cc9c --outcome answered --used /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body

2. **Answer**
For type E4, tenure T3, site L1 (current table, in force since 2026-01-01):
- Accrues 1.52 days per month.
- Carry-over limit is 10 days — the most you can still be holding (carried into January).

3. **Source**
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l1/body

4. **Notes**
The opening `/v1/regions/attendance` table listed `/v1/nodes/sec-hard-accrual` as a *table*, not the per-combination row files directly, so I put that table address (plus two plausible neighbors, `annual-leave` and `sec-days-that-decide-money`, in case "holding in January" meant a payout/settlement-day rule rather than a carry-over cap) into the overlay as members. Opening the overlay auto-expanded `sec-hard-accrual` into its 64 row files (one per type × tenure × site combination) plus its three legend files, so the exact row for E4/T3/L1 was right there without a second table hop. I read that row directly rather than the two other members — the row itself already answers both halves of the question (monthly accrual and carry-over limit), so `annual-leave` and `sec-days-that-decide-money` turned out to be unnecessary hedges. One mildly confusing bit: the overlay close output labelled the address I used as "reached ... from somewhere the overlay never named," even though it was printed as a row in the overlay's own table — seems to be because I named the parent table as the member, not the specific child row, so the tool doesn't count the auto-expanded row as an explicitly-named member. Worth knowing for next time: name the row-level address as a member up front if you already know the exact combination, to avoid that mismatch note.
