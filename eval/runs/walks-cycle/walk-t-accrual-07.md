1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body

2. Answer
Leave accrual has been written three times (two rewrites of an original). The three versions and their effective dates:
- Version 1 ("leave entitlement"): in force until 2024-07-01
- Version 2 ("leave accrual, second version"): in force 2024-07-01 to 2025-12-31
- Version 3 ("leave accrual, current"): in force from 2026-01-01 onwards (current as of today, 2026-09-22)

3. Source
/v1/nodes/hard-accrual-legend-revision/body (primary — states the three versions and their date ranges)
/v1/nodes/hard-accrual-v2/body (corroborates the 2024-07-01 to 2025-12-31 range and the boundaries with the other two versions)

4. Notes
The attendance table listed the current version (/v1/nodes/sec-hard-accrual) and the middle version (/v1/nodes/hard-accrual-v2/body) directly, but never printed an address for the oldest version — it's only referred to by name ("leave-accrual") inside body text, both in the legend-revision doc and in hard-accrual-v2's own body. Per the rules, I did not construct that address myself, so the oldest version's own document is not part of my source list even though its existence and date range are independently confirmed by two other documents. If a caller needs the oldest version's actual content (not just its date range), that would need to surface through some other table walk. Also worth flagging: the legend document explicitly warns that the oldest version's text does not mention being superseded, so naive keyword search on the corpus could easily surface it as if it were still current — the legend page is the load-bearing document here, not the tables themselves.
