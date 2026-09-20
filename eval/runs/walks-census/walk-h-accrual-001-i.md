1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body

2. **Answer**
Accrues 0.42 days per month. Carry-over limit (what you can still be holding into January) is 5 days.

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body

4. **Notes**
"On the regular payroll" is not an attendance-native term — it only resolves via the type legend, which maps it to E1. Easy to be thrown by the word "payroll" and detour into the payroll region; the legend at /v1/nodes/hard-accrual-legend-type confirms "on the regular payroll" is an employment-type qualifier for the accrual table, not a payroll-region question. The attendance region's top-level table flagged three versions of the accrual rules (a legend-revision warning) before showing the current one; since today (2026-09-20) falls after the 2026-01-01 effective date of `sec-hard-accrual`, the current table is correct and the two superseded versions (`hard-accrual-v2`, `leave-accrual`) were not needed. The three qualifiers (type/tenure/site) each needed their own legend lookup to convert plain-language phrasing ("been here eight months", "at the Busan branch") into the row's index codes (E1/T1/L2) — skipping any one of the three legends would have made it impossible to pick the right one of the 64 rows. The row itself answers both halves of the question directly (monthly accrual and carry-over limit), so no separate lookup was needed for the "how much can I still be holding in January" part — it maps straightforwardly onto "carry-over limit."
