1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py read /v1/nodes/leave-accrual/body

2. **Answer**: 15 days, granted whole on 1 January. (Two years of continuous service falls under the "1 year and over" band — 15 days flat; the +1-per-two-years increase only starts at 3 years and over, so it does not apply yet.)

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/accrual-rule/body
/v1/nodes/leave-accrual/body

4. **Notes**: The attendance region table only surfaces the two newer accrual versions (`hard-accrual-v2`, in force 2024-07-01 to 2025-12-31, and `sec-hard-accrual`, current from 2026-01-01) plus the legend page — the oldest version (`leave-accrual`, in force until 2024-07-01, which is the one that actually governs a September 2023 date) is not listed there at all. Without reading the legend first, the obvious next step from the attendance table would have been to open `hard-accrual-v2` and get the wrong version, since it's the only "old-looking" one visible at that level. The legend explicitly warns the oldest version "says nothing at all about having been replaced," so nothing in the old document itself would have flagged the mistake. The actual oldest table lives one level down, under `/v1/nodes/annual-leave`, reached by a completely different path than the other two versions. Also worth flagging: the table view of `leave-accrual` node gives a compressed one-line-per-band table, while the `/body` document gives the full prose version with the caveat that first-year monthly accrual and the January proration are not additive — not relevant to a two-year tenure but a plausible trap for a similarly-phrased question about a first-year joiner.
