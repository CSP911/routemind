1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 5 years tenure, Singapore entity: monthly leave accrual and January carry-forward cap" --member /v1/regions/attendance "leave accrual, part-time proration, carry-forward cap likely covered here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0053a6 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body

2. **Answer**
Accrues 1.24 days of leave per month. Carry-over limit (the most you can still be holding into the new year, e.g. January) is 12 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l3/body

4. **Notes**
There are three versions of the leave-accrual document (`leave-accrual` until 2024-07-01, `hard-accrual-v2` from 2024-07-01 to 2025-12-31, and `sec-hard-accrual` from 2026-01-01 onward), and a warning page explicitly flags that reaching for the newest table is wrong for any question dated before 2026-01-01. Today's date (2026-09-21) falls under the current table, so `sec-hard-accrual` was correct here, but this is an easy trap for any question with an earlier or unstated date — I checked the revision-legend page first specifically to avoid it.

The row is indexed by three separate legend translations rather than by the plain-language description: "in three days a week" → type E3, "been here five years" → tenure T3, "in the Singapore entity" → site L3. None of these codes are guessable from the question wording alone; each had to be looked up in its own legend file, and getting any one wrong (e.g. mistaking "two-year contract" type E2 for three-days-a-week type E3) would silently point at the wrong row without any error.

The overlay tool logged the five body pages as "reached ... from somewhere the overlay never named" rather than "used" cleanly, because I only registered `/v1/regions/attendance` as a member up front and never ran `overlay add` for the specific nodes as I drilled down — a cosmetic mismatch in how I worked the overlay, not a gap in the source data.
