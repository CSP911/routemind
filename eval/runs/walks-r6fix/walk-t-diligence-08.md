1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body

2. **Answer**: For a claim dated in 2025, the applicable version is the second/middle version of supplier due diligence — `hard-diligence-v2`, in force from 2024-07-01 to 2025-12-31 (indexed by two qualifiers: origin and value). It is neither the oldest version (until 2024-07-01, one qualifier) nor the current version (2026-01-01 onwards, three qualifiers, adds "goods"). The legend page at `hard-diligence-legend-revision` explicitly states this mapping of date-to-version and warns that a 2025 date is the one case where reaching for either extreme (oldest or current) is wrong.

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (states which version covers which date range)
/v1/nodes/hard-diligence-v2/body (confirms this is the version for 2024-07-01 to 2025-12-31, with its check-count table)

4. **Notes**: The procurement region table lists five due-diligence-related entries (`hard-diligence-legend-revision`, `hard-diligence-v2`, `sec-hard-diligence`, `sec-supplier-due-diligence`, plus the oldest `supplier-due-diligence` mentioned only inside the legend text, not as its own row in this table listing). It would be easy to jump straight to `sec-hard-diligence` since its row label calls it "THE CURRENT SUPPLIER DUE DILIGENCE TABLE" — but "current" means 2026-01-01 onwards, and a 2025-dated claim is explicitly the wrong case for that table. The legend-revision page exists precisely to catch this mistake and says so directly: "a date has to be checked rather than assumed." I read the legend first and it gave the full answer outright, so I didn't need to open `sec-supplier-due-diligence` (the four-page overview) or the oldest version at all.
