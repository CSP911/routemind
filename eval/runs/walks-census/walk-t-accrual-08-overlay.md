1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Which version of leave accrual applies to a claim dated in 2025?" --member /v1/regions/attendance "leave accrual policy versions likely documented in attendance region"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b12e4f --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-v2/body

2. **Answer**: A claim dated in 2025 is governed by the second (middle) version of leave accrual, in force 2024-07-01 to 2025-12-31, documented at `/v1/nodes/hard-accrual-v2/body`. This version indexes accrual by type and tenure (not yet by site, which was added in the 2026-01-01 current version). The legend/revision page at `/v1/nodes/hard-accrual-legend-revision/body` is the "where is that written down" pointer: it lays out all three versions and which date range each covers, and explicitly says a 2025 date maps to the middle version, not the oldest (`leave-accrual`) and not the current table (`sec-hard-accrual`).

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (the routing/legend page that says which version applies to which date range)
- /v1/nodes/hard-accrual-v2/body (the actual version-2 accrual table that applies to 2025 dates)

4. **Notes**: The attendance area's overlay table surfaced three separate "hard-accrual" nodes at once (`hard-accrual-legend-revision`, `hard-accrual-v2`, `sec-hard-accrual`), plus a parallel trio for overtime rate — easy to grab the wrong one if you didn't read the row descriptions carefully. The current table (`sec-hard-accrual`) is titled "THE CURRENT LEAVE ACCRUAL TABLE" with no date qualifier in its short blurb, which is the trap: for a 2025-dated claim, reaching for "current" is wrong, since current only means 2026-01-01 onward. The legend-revision page exists specifically to prevent that mistake and states outright that the oldest version says nothing about being superseded, so without checking dates first one could easily land on `leave-accrual` (pre-2024-07-01) or `sec-hard-accrual` (2026+) instead of the correct `hard-accrual-v2`. No ambiguity remained once the legend page was read — the date ranges are exact and non-overlapping.
