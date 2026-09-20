1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/leave-accrual/body

2. **Answer**
Leave accrual has been written three times (two rewrites of the original):
- Version 1 (original): in force until 2024-07-01. Indexed by one qualifier (length of service only). Does not itself mention being superseded.
- Version 2: in force from 2024-07-01 to 2025-12-31. Indexed by two qualifiers (type and tenure).
- Version 3 (current): in force from 2026-01-01 onwards. Indexed by three qualifiers (type, tenure, and site).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (primary — states all three versions and their date ranges)
/v1/nodes/hard-accrual-v2/body (confirms version 2's own range, 2024-07-01 to 2025-12-31, and cross-references the other two)
/v1/nodes/sec-hard-accrual (table header confirms current version in force from 2026-01-01, replacing `leave-accrual`)
/v1/nodes/leave-accrual/body (the original/oldest version — confirms it says nothing about being superseded, as the legend-revision doc warned)

4. **Notes**
The oldest version, "Leave entitlement" at /v1/nodes/leave-accrual, is a trap: it reads as if it's simply the current rule for length-of-service-based entitlement, with no mention anywhere in its own body of a successor or an end date. Without first reading hard-accrual-legend-revision, I'd have taken it at face value as still current. The legend-revision doc explicitly warns about this ("the oldest says nothing at all about having been replaced") and gives the only place where its 2024-07-01 end date is stated. I found /v1/nodes/leave-accrual by going through /v1/nodes/annual-leave, which is a different named node than the "hard-accrual" family; it's not obvious the two are the same subject until you compare the "leave entitlement" vs "leave accrual" wording and see hard-accrual-v2 and sec-hard-accrual both name `leave-accrual` explicitly as what they replace. The naming (leave "entitlement" vs "accrual") could easily mislead a search into thinking these are two separate topics rather than three sequential versions of one.
