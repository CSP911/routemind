1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body

2. **Answer**:
Accrues 0.98 days per month. Carry-over limit (the most you can be holding at the start of January) is 14 days.
(Row applies to type E2 — two-year contract, tenure T4 — nine years' service, site L2 — Busan branch; in force from 2026-01-01, which covers today's date of 2026-09-20.)

3. **Source**:
- /v1/regions/attendance (table)
- /v1/nodes/hard-accrual-legend-revision/body
- /v1/nodes/sec-hard-accrual (table)
- /v1/nodes/hard-accrual-legend-type/body
- /v1/nodes/hard-accrual-legend-tenure/body
- /v1/nodes/hard-accrual-legend-site/body
- /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l2/body

4. **Notes**:
The accrual subject has three superseding versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the legend-revision page warns explicitly that reaching for the newest table is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls inside the current version's range, so `sec-hard-accrual` was correct, but this was the one place it would have been easy to grab the wrong table without checking the in-force dates first.

Mapping "two-year contract" → type E2 was not obvious from the question's phrasing alone — the legend's wording ("on a two-year contract") matched exactly, so no ambiguity there. Same for "nine years" → T4 (exact match, no need to round to nearest band) and "Busan branch" → L2 (exact match). Had any of these not matched exactly, the legends' instruction to "take the nearest entry above it" would have applied, which is a judgment call worth flagging if it ever comes up.

The row's own text doubles as the answer to "how much can still be held in January" — the carry-over limit (14 days) is exactly that cap, so no separate lookup was needed for the second half of the question. The row's "if exceeded" clause was read but not needed since the question doesn't describe an excess situation.
