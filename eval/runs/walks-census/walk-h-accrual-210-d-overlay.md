1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T2, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carry-over/cap rules by employee type, tenure, site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_3cebd8 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body

2. **Answer**
Accrues 1.12 days per month. Carry-over limit (what can still be held going into January) is 7 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l1/body

4. **Notes**
This subject has three versions in force at different date ranges (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward). Today's date (2026-09-20/21) falls in the current window, so the current table `sec-hard-accrual` is correct — but this is exactly the kind of question where grabbing the newest-looking table without checking the revision-legend first would have been a mistake if the question had been dated in 2025. Worth flagging: the row's own file confirms "In force from 2026-01-01," which double-checks the date choice was right. The row for E3/T2/L1 existed as a direct, exact match in the current table's index — no legend lookups for type/tenure/site codes were needed since the address itself was already keyed by those exact codes. The overlay tool noted the two addresses I used were "reached... from somewhere the overlay never named" since I never explicitly added them as overlay members (I only added the parent region as a member and then drilled down) — worth using `overlay add` for the specific rows next time to avoid that note, though it didn't affect the outcome.
