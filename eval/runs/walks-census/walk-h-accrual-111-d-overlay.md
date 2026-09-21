1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T2, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carry-over/holding cap by employee type, tenure, and site"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b51158 --outcome answered --used /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body

2. **Answer**: For type E2, tenure T2, site L2: accrues 0.82 days per month. Carry-over limit (the most you can be holding into the new year, i.e. into January) is 8 days.

3. **Source**:
- /v1/nodes/sec-hard-accrual (table listing the current accrual rows, used to locate the E2/T2/L2 row)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l2/body (the row with the actual figures)

4. **Notes**: The attendance table surfaced a scary-looking warning node (`hard-accrual-legend-revision`) saying leave accrual has three versions with different dates, plus a superseded `hard-accrual-v2` node for 2024-07-01–2025-12-31. It would be easy to grab the wrong version here. I didn't need to open the legend-revision doc because the row I read states its own effective date plainly ("In force from 2026-01-01") and today (2026-09-20/21) falls inside that range, so `sec-hard-accrual` is the correct, currently-active table — no ambiguity in the end, but the versioning warning is the kind of thing that could easily trip up a faster pass. Also worth flagging: the question's phrase "how much can I still be holding in January" maps to the row's "Carry-over limit" field — the table doesn't use the word "January" or "holding" anywhere, so that mapping is an inference, not a literal match.
