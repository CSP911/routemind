1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "On a two-year contract, been here nine years, fully from home: how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual, monthly accrual rate, carryover/holding cap questions"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_647748 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**:
Accrues 1.02 days per month. Carry-over (holding) limit is 16 days — that is the most that can still be held going into January.

3. **Source**:
- /v1/nodes/hard-accrual-legend-type/body (two-year contract → type E2)
- /v1/nodes/hard-accrual-legend-tenure/body (nine years → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body (fully from home → site L4)
- /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l4/body (1.02 days/month accrual, 16-day carry-over limit)
- /v1/nodes/hard-accrual-legend-revision/body (confirms the 2026-01-01-onwards table, `sec-hard-accrual`, is the correct version for both today, 2026-09-20, and January)

4. **Notes**:
The three qualifiers (contract type, tenure, site) each needed their own legend lookup before the row address could be built — none of them are guessable from the question's wording, they have to be translated word-for-word through the legend tables (e.g. "two-year contract" → E2, not the more literal-sounding E3 "three days a week"). Easy to misassign these without reading all three legends carefully.

The bigger trap was version: there are three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges, and the question mentions January, which could have tempted a check against "next year's" rules if misread as a future date. Confirmed via the revision legend that both today's date and January both fall under the current (2026-01-01 onward) table, so no version mismatch — but this is exactly the kind of question where grabbing the newest table without checking the date range would happen to be right for the wrong reason, or wrong if the question were instead dated in 2025.

The overlay close reported all five addresses as "reached ... from somewhere the overlay never named" rather than as formal matches, because I only registered the top-level `/v1/regions/attendance` table as a member and then navigated onward via `table`/`read` without doing `overlay add` for each specific node. Functionally the answer is the same, but the overlay's own bookkeeping doesn't show a tidy narrowed set — worth doing explicit `overlay add`/`remove` steps in future walks for a cleaner audit trail.
