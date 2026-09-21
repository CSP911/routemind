1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For origin O2, value W1, goods K4, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/regions/procurement "goods/value/origin risk factors and site-visit/review-frequency rules sound like vendor due diligence under procurement"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a41eff --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body

2. **Answer**
Site visit: no. Re-review interval: every 36 months.
(For reference, this row also carries: screening score required 49, financial statements not required.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established which of the three versions applies for today's date, 2026-09-20)
- /v1/nodes/sec-hard-diligence (the current table, confirmed the exact row address for origin O2/value W1/goods K4)
- /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body (the answer itself)

4. **Notes**
The supplier due diligence subject has three superseded/current versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend page is explicit that the oldest version says nothing about being replaced — so grabbing the first due-diligence table found without checking the revision legend would have silently produced a stale answer. Today's date (2026-09-20) falls after the 2026-01-01 start of the current table, so `sec-hard-diligence` was correct; a 2025-dated question would have needed the middle version instead, which is the specific trap the legend calls out. Once the correct table version was confirmed, the origin/value/goods-coded row address was a direct, unambiguous match — no further narrowing needed. The row's closing paragraph about "excess" and budget-holder claims reads like boilerplate carried over from an expense/reimbursement template and has nothing to do with site visits or review intervals; it was ignored.
