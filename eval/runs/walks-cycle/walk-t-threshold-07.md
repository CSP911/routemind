1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/procurement-overview/body

2. Answer
The approval threshold has been rewritten twice (three versions total, two rewrites):
- Version 1 (oldest): in force until 2024-07-01. Indexed by one qualifier (amount only, no category or term). Start date not stated anywhere I could read.
- Version 2: in force from 2024-07-01 to 2025-12-31. Indexed by two qualifiers (category and amount).
- Version 3 (current): in force from 2026-01-01 onwards. Indexed by three qualifiers (category, amount, and term).

3. Source
/v1/nodes/hard-threshold-legend-revision/body (names all three versions and the date boundaries)
/v1/nodes/hard-threshold-v2/body (confirms version 2's dates and that version 1 was called `threshold-table`)
/v1/nodes/sec-hard-threshold (confirms current version 3 is in force from 2026-01-01, replacing `threshold-table` and "the older rules around it")

4. Notes
The oldest version is referred to by name only, as `threshold-table`, inside the body text of hard-threshold-legend-revision and hard-threshold-v2 — it never appeared as a full address in any `table` command output I ran (the /v1/regions/procurement table listed only the legend-revision file, the v2 file, and the current sec-hard-threshold table, not a third file for the oldest version). Per the rule against constructing addresses, I did not guess a path like /v1/nodes/threshold-table to read it directly, so I cannot report its start date or confirm details of its content beyond what the legend and v2 pages already summarize (single-qualifier, amount-only). If a start date for version 1 exists, it lives in a document I could not reach through a printed table address.

The near-miss to flag: the legend-revision page itself warns that "reaching for the newest is wrong for anything before 2026-01-01" and that a 2025-dated question needs the middle (v2) version, not the current or oldest one — easy to get wrong if you stop at the current sec-hard-threshold table without checking the legend page first.
