1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 8 months tenure, Singapore entity: monthly leave accrual rate and max carry-forward/holding balance allowed in January" --member /v1/regions/attendance "leave accrual, mid-year joiner leave, and carry-forward rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_1d2504 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body

2. **Answer**
Accrues 1.40 days of leave per month. Carry-over limit into the new year (what can still be held in January) is 6 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l3/body

4. **Notes**
There are three versions of the leave accrual table (pre-2024-07-01, 2024-07-01–2025-12-31, and current from 2026-01-01), and the legend-revision page warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01. Since today's walk date (2026-09-20) falls after 2026-01-01, the current table `sec-hard-accrual` was the correct one to use — but this was a real branch point where picking the wrong version (e.g. `hard-accrual-v2`, superseded but not marked as such on its own page) would have given a plausible-looking but wrong answer. All three qualifiers in the question mapped onto the legends as exact phrase matches ("here from our partner firm" → E4, "been here eight months" → T1, "in the Singapore entity" → L3), so no fuzzy nearest-match judgment call was needed here. One ambiguity worth flagging: the question asks "how much can I still be holding in January" — I read this as the carry-over limit (6 days), since that's the figure that governs what balance survives into the new year, but the table doesn't use the word "January" itself, so this is an interpretive link rather than a literal label match.
