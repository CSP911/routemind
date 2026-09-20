1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body

2. **Answer**: 0.56 days accrue per month. Up to 10 days may be carried over into January (the carry-over limit).

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body

4. **Notes**: The attendance table lists three vintages of the leave-accrual subject (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) and warns explicitly that reaching for the newest is wrong for any date before 2026-01-01 — the oldest page doesn't announce that it's been superseded. Today (2026-09-20) falls under the current table, `sec-hard-accrual`, so that part was safe, but it's the kind of trap that would silently give a wrong number for a 2025-dated question. The three qualifiers ("regular payroll" → E1, "five years" → T3, "Seoul office" → L1) each had an exact match in their legend, so no nearest-value judgment call was needed here — worth flagging only because the legends explicitly allow for inexact matches and I didn't need that fallback. The row itself answers both halves of the question directly (monthly accrual and carry-over limit), so nothing needed to be inferred or combined from a second row.
