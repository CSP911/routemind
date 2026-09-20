1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body

2. **Answer**: Accrues 0.92 days per month. Carry-over limit is 12 days — that is the most that can still be held in January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l3/body

4. **Notes**: This table has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is wrong for anything before 2026-01-01 — today's date (2026-09-20) falls under the current table, so that risk didn't materialize here, but it's the kind of thing that's easy to skip past. The bigger trap was the three legends: "two-year contract" maps to type E2, not tenure — it's easy to misread it as "been here two years" (tenure T2) since both phrases mention "two years." The tenure legend separately keys off actual time in the company ("been here five years" → T3), and the two must not be conflated. Also worth flagging: the row's entitlement table only labels one figure "Carry-over limit, days" (12) — the question's "how much can I still be holding in January" maps to that cap, not to the monthly accrual rate; the two numbers (0.92 accrual vs. 12 cap) are easy to mix up if skimmed quickly.
