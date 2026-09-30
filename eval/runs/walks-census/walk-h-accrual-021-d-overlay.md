1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E1, tenure T3, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carry/cap rules by employee type, tenure, site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_639f4a --outcome answered --used /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body

2. **Answer**:
Accrues 0.58 days per month. Carry-over limit (the most that can still be held) is 11 days. This is the table in force from 2026-01-01 onward, which covers today's date.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual table versions applies to today's date)
- /v1/nodes/sec-hard-accrual (the current accrual table, opened to find the E1/T3/L2 row)
- /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body (the row with the actual figures: 0.58 days/month accrual, 11 days carry-over limit)

4. **Notes**:
Leave accrual has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page is explicit that reaching for the newest one is wrong for any date before 2026-01-01. Today's date (2026-09-20/21) falls under the current table, so no trap here, but it would have been easy to skip that check and just grab the first accrual-looking table found — the overlay's row list surfaces `hard-accrual-v2` and `sec-hard-accrual` right next to each other with very similar names, and skipping the version check is exactly how you'd answer with a stale rate.

The question already gave the codes (E1/T3/L2) directly rather than descriptive terms, so I didn't need the legend-site/tenure/type translation pages — went straight to the matching row address in the table listing.

"How much can I still be holding" was interpreted as the carry-over limit (11 days), which is the figure on the row that caps how much accrued leave can be held/carried rather than paid out or forfeited. No separate "January" rule was found on the row or in the table's own description beyond the general 2026-01-01-onward effective date, so the January framing in the question is read as referring to carry-over into the new year, not a distinct value in the corpus.

The overlay close reported both used addresses as "reached" rather than as directly-named overlay members — I had navigated to `sec-hard-accrual` via the table listing and to the row via that table's own listing, rather than adding them explicitly with `overlay add`. Worth noting since it means the overlay's own membership list undercounts what was actually walked.
