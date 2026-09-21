1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For something dated 29 June 2024 - two days before the first change - what screening was required for a new supplier? Use the version in force on that day." --member /v1/regions/procurement "supplier screening likely under procurement policy"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py overlay close --id ov_2026-09-20_11a848 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-supplier-due-diligence /v1/nodes/supplier-due-diligence/body

2. **Answer**: Under the version of supplier due diligence in force until 2024-07-01 (which covers 29 June 2024, two days before the first change on 2024-07-01), a new supplier had to pass three checks before registration:
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen — whether the entity or its owners had been flagged before
A sanctions hit or a refused code of conduct stops registration outright, with no delegated sign-off able to override it. The purchasing desk runs the initial check; ambiguous cases (shared director, holding company layers) go to the division head, not back to the requester.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (established the version timeline: oldest version in force "until 2024-07-01", second version from 2024-07-01 — confirming 29 June 2024 falls in the oldest version, two days before that first change)
- /v1/nodes/sec-supplier-due-diligence (table listing the four due-diligence pages, used to find the address of the oldest supplier-due-diligence document)
- /v1/nodes/supplier-due-diligence/body (the oldest version's document — actual content of the answer)

4. **Notes**: The legend-revision page doesn't print full addresses, only short names like `supplier-due-diligence` — had to go back to the table (sec-supplier-due-diligence) to get the actual printed address rather than guessing one. The overlay's working set initially listed `hard-diligence-v2` prominently (the 2024-07-01 to 2025-12-31 version), which would have been the wrong pick — the question's date of 29 June 2024 is two days *before* that version took effect, so the oldest, unnamed version at `/v1/nodes/supplier-due-diligence/body` is the correct one. The legend explicitly warns that "the oldest says nothing at all about having been replaced," which matches the document I read — it makes no mention of a successor, so without the legend page it would have looked like the current/only version.
