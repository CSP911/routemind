1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body

2. **Answer**
Under the version of supplier due diligence in force until 2024-07-01 (which covers March 2023), a new supplier had to pass three checks before registration:
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen (whether the entity or its owners had been flagged before)

A sanctions hit or a refused code of conduct stopped registration outright, with no delegated sign-off able to override it.

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (dates the three versions; confirms March 2023 falls under the oldest, "one qualifier" version)
/v1/nodes/supplier-due-diligence/body (the actual checks, oldest version)

4. **Notes**
The oldest version's address (`supplier-due-diligence`) is not listed in the `/v1/regions/procurement` table itself — that table only surfaces `hard-diligence-v2` and `sec-hard-diligence` directly, plus the legend page. The oldest page is only reachable one hop further, via `/v1/nodes/sec-supplier-due-diligence` ("where to start"). A walk that stopped at the procurement table's file rows could easily default to `hard-diligence-v2` (superseded, 2024-07-01 to 2025-12-31) as "the old one" and get March 2023 wrong, since v2 is the more prominent/older-looking option sitting right there.

The legend page explicitly warns that the oldest version's own text "says nothing at all about having been replaced" — confirmed: `supplier-due-diligence/body` reads like a live, current policy with no date markers or superseded notice. Without reading the legend first, there'd be no way to tell this page wasn't current. Checking the legend before trusting content on any of these due-diligence pages was the deciding step.
