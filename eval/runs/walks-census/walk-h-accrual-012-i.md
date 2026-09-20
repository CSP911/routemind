1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body

2. **Answer**: 0.52 days accrue per month. The carry-over limit is 9 days — the most you can still be holding when the year turns over into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body

4. **Notes**: Two traps here, both worth flagging. First, this subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) and the legend-revision page warns not to reflexively grab the newest — today (2026-09-20) does fall under the current table (in force since 2026-01-01), but a question dated in 2025 would need `hard-accrual-v2` instead, and that older page gives no hint it was ever replaced. Second, and more dangerous: "on the regular payroll" and "been here two years" look like they could both describe employment type, but the type legend maps "on the regular payroll" to E1 and separately "on a two-year contract" to E2 — a two-year *contract* is a different axis (type) from having *tenure* of two years (which is T2 on the tenure legend). Mixing those up would have pulled row E2/T2/L3 instead of the correct E1/T2/L3, silently changing the answer. Also worth noting: "how much can I still be holding in January" is answered by the row's carry-over limit field, not a separate January-specific document — there was no dedicated node for year-end carryover timing, so I inferred it's the same figure the row already states.
