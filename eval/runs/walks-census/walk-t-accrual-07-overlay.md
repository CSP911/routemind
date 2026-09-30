1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "How many times has leave accrual been rewritten, and from what date does each version apply?" --member /v1/nodes/hard-accrual-legend-revision/body "warning page listing all versions of leave accrual and their date ranges" --member /v1/nodes/hard-accrual-v2/body "superseded version 2024-07-01 to 2025-12-31" --member /v1/nodes/sec-hard-accrual "current version in force from 2026-01-01"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay add --id ov_2026-09-20_2cf01d --address /v1/nodes/leave-accrual --why "oldest version, in force until 2024-07-01, per legend-revision table"
./bench/rmcli.py overlay close --id ov_2026-09-20_2cf01d --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**:
Leave accrual has been written three times:
- Version 1 ("Leave entitlement", node `leave-accrual`) — in force until 2024-07-01.
- Version 2 ("Leave accrual, second version", node `hard-accrual-v2`) — in force from 2024-07-01 to 2025-12-31.
- Version 3, current ("Leave accrual", node `sec-hard-accrual`) — in force from 2026-01-01 onwards.
None of the three were formally withdrawn; the applicable version depends on the date of the question. A question dated in 2025 is answered by the second (middle) version, not the oldest or the current one.

3. **Source**: /v1/nodes/hard-accrual-legend-revision/body

4. **Notes**: The attendance table's row for this legend-revision file already flags in its own description that leave accrual "has THREE versions with different..." — that one-line warning was enough to know this was the right (and only) document needed; no need to open the three underlying version tables themselves. Adding /v1/nodes/leave-accrual and /v1/nodes/sec-hard-accrual to the overlay as members was a slight misstep: both are tables rather than single documents, so each expanded into dozens of unrelated per-type/tenure/site row addresses that cluttered the working set without adding anything — the legend-revision page had already given the full three-version answer including exact node names and date ranges, so those rows were never read.
