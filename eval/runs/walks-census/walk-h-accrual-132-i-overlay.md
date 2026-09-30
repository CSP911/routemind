1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two-year contract, nine years tenure, Singapore entity: monthly leave accrual rate and January carry-forward cap" --member /v1/regions/attendance "leave accrual, carry-forward, and contract/tenure rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_66119e --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body

2. **Answer**
Accrues 1.00 day of leave per month. Carry-over limit is 15 days — that is the most you can still be holding once the new year (January) starts; any unapproved excess above it is forfeited at year-end and not recoverable.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (established that the 2026-01-01-onward table, `sec-hard-accrual`, is the one in force for a 2026-09-20 question)
/v1/nodes/hard-accrual-legend-type/body (two-year contract → type E2)
/v1/nodes/hard-accrual-legend-tenure/body (nine years → tenure T4)
/v1/nodes/hard-accrual-legend-site/body (Singapore entity → site L3)
/v1/nodes/hard-accrual-row-type-e2-tenure-t4-site-l3/body (the row itself: 1.00 day/month accrual, 15-day carry-over limit)

4. **Notes**
- The revision-legend warning is the whole game here: `sec-hard-accrual` (current), `hard-accrual-v2` (2024-07-01 to 2025-12-31), and the original `leave-accrual` all coexist with no cross-references, and the oldest doesn't admit it's been superseded. Today (2026-09-20) is safely inside the current table's window, but if this had been a 2025-dated question I'd have needed `hard-accrual-v2` instead — grabbing the newest table on reflex would have been wrong there.
- "How much can I still be holding in January" reads at first like a question about remaining leave balance, but the row's "Carry-over limit" field is clearly the intended match — it's the cap on what survives into the new year, which is exactly what's asked. No separate "January" or year-end rule appeared anywhere else in the attendance area.
- Nine years landed exactly on tenure T4's stated band ("been here nine years"), and Singapore landed exactly on site L3 — no nearest-neighbor judgment call needed for either, unlike the type mapping where "two-year contract" required picking the literal matching line (E2) rather than reasoning from first principles about contract types.
- The overlay's own table only listed `sec-hard-accrual` at the top level; the legend and row files sit one level deeper (under `table /v1/nodes/sec-hard-accrual`), so `overlay close` reported all five used addresses as "reached" rather than pre-named members. That's expected given how the overlay was scoped, not a sign anything was fetched improperly.
