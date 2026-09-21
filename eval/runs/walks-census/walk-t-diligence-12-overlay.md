1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "We are reconciling claims from 2023 and from 2025 against supplier due diligence. Which two versions do I need, and what screening was required under each?" --member /v1/regions/procurement "supplier due diligence and screening requirements are procurement policy territory"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py overlay add --id ov_2026-09-20_8bef18 --address /v1/nodes/supplier-due-diligence/body --why "oldest version, in force until 2024-07-01, covers 2023 claims"
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/hard-diligence-v2
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay close --id ov_2026-09-20_8bef18 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/supplier-due-diligence/body /v1/nodes/hard-diligence-v2/body

2. **Answer**:

Supplier due diligence has been written three times, and the date on each claim decides which version applies:

- **2023 claims → the oldest version**, `/v1/nodes/supplier-due-diligence/body` (in force until 2024-07-01). Screening required (uniform, not varied by origin/value/goods):
  - A sanctions and ownership check against the current restricted-party lists
  - A supplier code of conduct acknowledgement, signed by the supplier
  - A basic disqualification screen (has this entity or its owners been flagged before)
  - A sanctions hit or refused code of conduct stops registration outright, with no delegated override; a hit found after registration triggers the same suspension/freeze as one found before.

- **2025 claims → the second version**, `/v1/nodes/hard-diligence-v2/body` (in force 2024-07-01 to 2025-12-31). Screening required was indexed by two qualifiers — origin (O1–O4) and contract value (W1–W4) — via this matrix of check codes:

  | origin \ value | W1 | W2 | W3 | W4 |
  |---|---|---|---|---|
  | O1 | 30 | 31 | 32 | 33 |
  | O2 | 34 | 35 | 36 | 37 |
  | O3 | 38 | 39 | 40 | 41 |
  | O4 | 42 | 43 | 44 | 45 |

  No legend translating these check codes (30–45) into named checks exists in this version's node or anywhere else reachable from the procurement region — the source does not go further than the matrix itself. Everything else (documents to collect, re-review interval) followed the oldest version's rule unchanged.

Do not use the current table, `/v1/nodes/sec-hard-diligence` (in force from 2026-01-01, three qualifiers including goods) — it postdates both 2023 and 2025.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (establishes which of the three versions covers which date range)
- /v1/nodes/supplier-due-diligence/body (2023 version and its screening requirements)
- /v1/nodes/hard-diligence-v2/body (2025 version and its screening matrix)

4. **Notes**:
The overlay created from `/v1/regions/procurement` surfaced the legend-revision and v2 pages directly, but not the oldest version's address — that one only had an explicit WARNING that the oldest page "says nothing at all about having been replaced," which is exactly what made it easy to miss. Found it by opening `/v1/nodes/sec-supplier-due-diligence` (a "where to start" table) and finding `/v1/nodes/supplier-due-diligence/body` listed among its four due-diligence pages. Without the legend-revision page, the natural mistake here would have been to answer 2025 with the *current* table (`sec-hard-diligence`) since it's flagged "current" and shows up first/most prominently — the legend explicitly calls this out as the wrong extreme, since the current table only took effect 2026-01-01, after both dates in question. The v2 matrix's numeric codes (30–45) have no decoding available anywhere in the procurement region (confirmed by listing the full unfiltered region table) — reported as-is rather than guessed at.
