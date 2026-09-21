## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/leave-accrual/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual

## Answer
Leave accrual has been written three times (the original, plus two rewrites):
1. Original version ("Leave entitlement") — in force until 2024-07-01. No start date given (it predates the versioning scheme); indexed by one qualifier (length of service only).
2. Second version ("Leave accrual, second version") — in force from 2024-07-01 to 2025-12-31; indexed by two qualifiers (type and tenure).
3. Current version ("Leave accrual, current") — in force from 2026-01-01 onward; indexed by three qualifiers (type, tenure, and site).

## Source
- /v1/nodes/hard-accrual-legend-revision/body (the revision legend — states three versions and their date ranges)
- /v1/nodes/leave-accrual/body (the original/oldest version, confirms content but not an explicit start date)
- /v1/nodes/hard-accrual-v2/body (second version, confirms 2024-07-01 to 2025-12-31 in its own text)
- /v1/nodes/sec-hard-accrual (current version table header, confirms in force from 2026-01-01)

## Notes
The attendance table listing surfaces /v1/nodes/hard-accrual-v2/body and /v1/nodes/sec-hard-accrual directly, but not the oldest version's address — that one is under /v1/nodes/annual-leave → /v1/nodes/leave-accrual, reached via a different path (Annual leave, not the "hard-accrual" naming family). If I had only browsed the attendance table's flat list, I'd have concluded there were only two versions and missed the oldest one entirely. The legend doc at hard-accrual-legend-revision explicitly warns about this trap: "the oldest says nothing at all about having been replaced," and its own text is what pointed me to the `leave-accrual` address to go find the first version and confirm it. Also worth flagging: the oldest version's own body text carries no explicit effective-date language (no "in force from/until" line like the other two have) — its start/end boundary is only stated in the legend doc, not in the source document itself, so that date rests on the legend's authority rather than the original page's own words.
