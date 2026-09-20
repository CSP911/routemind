1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py read /v1/nodes/sec-hard-diligence

2. **Answer**
Supplier due diligence has been rewritten twice (three versions total):
- Version 1 (original): in force until 2024-07-01
- Version 2: in force from 2024-07-01 to 2025-12-31
- Version 3 (current): in force from 2026-01-01 onwards

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (states all three versions and their date ranges explicitly)
- /v1/nodes/supplier-due-diligence/body (the oldest version, confirmed to exist; contains no date of its own)
- /v1/nodes/hard-diligence-v2/body (second version, confirms "in force from 2024-07-01 until 2025-12-31")
- /v1/nodes/sec-hard-diligence (current version, confirms "in force from 2026-01-01")

4. **Notes**
The procurement area table lists both a "legend-revision" WARNING page and the current/previous tables side by side, which could tempt reading just the current table (`sec-hard-diligence`) and missing that two older versions exist — the current table's own one_liner only mentions replacing `supplier-due-diligence` (the oldest) and doesn't mention the intermediate `hard-diligence-v2` by name, which could mislead someone into thinking there were only two versions. The `hard-diligence-legend-revision` page is the one that spells out all three unambiguously and explicitly warns that the oldest version "says nothing at all about having been replaced," so it would look self-contained and current if found on its own. Cross-checking against `hard-diligence-v2`'s body (which explicitly names both its predecessor and successor) resolved any doubt. The oldest version's document address (`supplier-due-diligence`) was only available as a bare index name in the legend table, not a usable address — I got the real address only by opening `/v1/nodes/sec-supplier-due-diligence` (the "where to start" overview), which listed it properly.
