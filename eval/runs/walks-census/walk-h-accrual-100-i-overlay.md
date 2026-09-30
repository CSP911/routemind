1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "On a two-year contract, been here eight months, at the Seoul office: how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/holding cap likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_14423b --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body

2. **Answer**:
Accrues 0.72 days per month. Carry-over limit is 4 days — that is the most that can still be held over into January (the new year).

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l1/body

4. **Notes**:
The main trap here is the three coexisting versions of the leave accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), with the legend page warning that "the oldest says nothing at all about having been replaced" — grabbing the first hit without checking the revision legend would silently give a 2024-era or pre-2024 rule. Today's date (2026-09-20/21) falls in the current table's force period (2026-01-01 onward), so `sec-hard-accrual` was correct, but this would have been wrong for any question dated in 2025.

The three qualifiers (type/tenure/site) each needed their own legend lookup rather than guessing — "two-year contract" maps to type E2 (not tenure!), which is an easy mix-up since "two-year" sounds like a tenure duration but is actually the contract-type qualifier. Tenure is instead keyed off "been here eight months" → T1. All three qualifiers happened to be exact matches in their legends (no need to fall back to "nearest entry"), so no ambiguity there.

The overlay close reported all five read addresses as "reached" rather than "used," since I never formally added them as overlay members (I only added the parent `/v1/regions/attendance` area) — cosmetic, doesn't affect the answer, but worth noting the overlay's own bookkeeping distinguishes members you declared from pages you merely visited.
