1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "In January 2024, what screening was required for a new supplier? Answer under the version of supplier due diligence in force on that date." --member /v1/nodes/hard-diligence-legend-revision/body "explains which version of supplier due diligence covers which date range" --member /v1/nodes/hard-diligence-v2/body "version in force 2024-07-01 to 2025-12-31, need to check if Jan 2024 falls in an earlier version" --member /v1/nodes/sec-hard-diligence "current table, in force from 2026-01-01, not applicable to Jan 2024 but useful for structure"
./bench/rmcli.py overlay remove --id ov_2026-09-20_f4f658 --address /v1/nodes/sec-hard-diligence --why "fanned out into 64 unrelated combination rows for the current 2026 table; not needed for a Jan 2024 question"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_f4f658 --address /v1/nodes/hard-diligence-v2/body --why "covers 2024-07-01 to 2025-12-31; Jan 2024 predates this, so the oldest version applies instead"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py overlay add --id ov_2026-09-20_f4f658 --address /v1/nodes/supplier-due-diligence/body --why "this is the oldest version (in force until 2024-07-01), the one that governs Jan 2024, indexed by one qualifier"
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f4f658 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-supplier-due-diligence/body /v1/nodes/supplier-due-diligence/body

2. **Answer**:
Under the version of supplier due diligence in force in January 2024 (the oldest version, in force until 2024-07-01), a new supplier had to pass three checks before registration:
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen — whether the entity or its owners had been flagged before
The purchasing desk runs the initial check when the vendor form comes in; anything ambiguous (e.g. a shared director, a holding company layers up) goes to the division head handling the account. A sanctions hit or a refused code of conduct stops registration outright, with no delegated sign-off able to override it.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (established which of the three versions covers January 2024)
- /v1/nodes/sec-supplier-due-diligence/body (hub page, needed to find the exact address of the oldest version — it was not listed by that address in the procurement table)
- /v1/nodes/supplier-due-diligence/body (the actual answer — the version in force until 2024-07-01)

4. **Notes**:
The procurement table lists three due-diligence-related entries whose titles all mention "current," "second version (2024-07-01 to 2025-12-31)," etc., but never spells out an address for the oldest/first version — its full path (`/v1/nodes/supplier-due-diligence/body`) only surfaced after reading the legend-revision page, which named it by short name ("supplier-due-diligence"), and then going through the `sec-supplier-due-diligence` hub table to get the exact printed address. Guessing `/v1/nodes/supplier-due-diligence/body` from the short name would have violated the "never construct an address" rule, so the hub detour was necessary.
The near-miss: my first instinct was to reach for `/v1/nodes/hard-diligence-v2/body` since it was the version literally named in the procurement table's row listing and looked most "official" for a 2024 date. Reading the legend-revision page first was what caught this — v2 only starts 2024-07-01, so a January 2024 question falls under the oldest, unlisted version instead. The legend page explicitly warns that this exact trap (assuming the second version covers all of 2024) is the case worth being careful about.
Also wasted a step adding `/v1/nodes/sec-hard-diligence` (the current 2026 table) to the working set — it silently expanded into 64 per-origin/value/goods combination row addresses, none relevant, and had to be removed.
