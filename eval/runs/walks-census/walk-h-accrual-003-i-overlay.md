1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Regular payroll, 8 months tenure, fully remote/home-based: monthly leave accrual rate and max balance holdable in January" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site - since 2026-01-01"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_95bba3 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body

2. **Answer**:
Accrues 0.46 days per month. The carry-over limit is 7 days — that is the most you can still be holding once the year turns to January (any unapproved excess above that is settled at 7 days and not recoverable).

3. **Source**:
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body

4. **Notes**:
"Regular payroll" is not a term the accrual table uses directly — it only appears as a value in the type legend ("on the regular payroll" → type E1). Same for "been here eight months" (→ tenure T1) and "fully from home" (→ site L4). Without reading the three legend files first, there'd be no way to know which of the 64 per-row files (E1–E4 × T1–T4 × L1–L4) applies; the row addresses give no hint from employment/tenure/site English descriptions, only the E/T/L codes. The overlay's initial member was the parent table (sec-hard-accrual), not the individual row/legend files — closing with those four addresses in `--used` got them marked "reached" rather than pre-declared members, which the tool flagged but did not treat as an error. Also worth flagging: the sec-hard-accrual table is explicitly the version in force from 2026-01-01, and today is 2026-09-20, so this is the correct, current table — older versions (hard-accrual-v2, leave-accrual) exist and would give different figures if mis-picked. The question's "how much can I still be holding in January" was interpreted as the carry-over limit (7 days), since that's the figure governing balance held across the year boundary; the table doesn't have a separate "January" figure.
