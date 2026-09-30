1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "What screening was required for a new supplier in 2023, and what had it become by 2025?" --member /v1/nodes/hard-diligence-legend-revision/body "explains which diligence version covers which date range" --member /v1/nodes/hard-diligence-v2/body "version in force 2024-07-01 to 2025-12-31, covers 2025" --member /v1/nodes/sec-hard-diligence "current table, in force from 2026-01-01, for context only"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py overlay add --id ov_2026-09-20_f6b757 --address /v1/nodes/supplier-due-diligence/body --why "oldest version, in force until 2024-07-01, covers 2023"
./bench/rmcli.py overlay remove --id ov_2026-09-20_f6b757 --address /v1/nodes/sec-hard-diligence --why "current table (2026-01-01 onwards), not relevant to 2023 or 2025 question"
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/hard-diligence-v2
./bench/rmcli.py overlay close --id ov_2026-09-20_f6b757 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/supplier-due-diligence/body /v1/nodes/hard-diligence-v2/body

2. **Answer**
In 2023 (rule in force until 2024-07-01), a new supplier had to clear a single flat screen with no qualifiers by origin, value, or goods type — three checks, run by the purchasing desk when the vendor form came in:
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen (whether the entity or its owners had been flagged before)
A sanctions hit or a refused code of conduct stopped registration outright, with no delegated sign-off able to override it; a hit found after registration was treated the same as one found before (suspension, open POs frozen).

By 2025 (the second version, in force 2024-07-01 to 2025-12-31), the screen was no longer flat: it was indexed by two qualifiers — supplier origin (O1–O4) and contract value band (W1–W4) — as a 4×4 matrix of numbered check levels (e.g. O1/W1 = check 30, up to O4/W4 = check 45). The document itself does not carry a legend translating those check numbers into specific requirements. Everything else — which documents to collect and the re-review interval beyond that matrix — followed the 2023 rule unchanged until 2026-01-01, when a third qualifier (goods category) and a new current table (sec-hard-diligence) took over.

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established which of the three versions applies to which date range)
- /v1/nodes/supplier-due-diligence/body (2023 answer — the oldest, one-qualifier version)
- /v1/nodes/hard-diligence-v2/body (2025 answer — the two-qualifier version, 2024-07-01 to 2025-12-31)

4. **Notes**
The procurement region table only surfaced the legend-revision doc, the v2 doc, and the current (sec-hard-diligence) doc directly — the oldest version (supplier-due-diligence/body) wasn't listed there at all, and its absence could easily read as "there is no 2023 version, so use the oldest thing shown." The legend-revision doc explicitly warns against exactly that assumption. The oldest doc only turned up by going one level further, through the unrelated-looking "where the four due-diligence pages fit together" table (sec-supplier-due-diligence), which is where it was actually indexed. Also, opening sec-hard-diligence to get there caused the overlay to balloon to 69 rows (it expanded into ~64 origin/value/goods leaf rows for the *current*, 2026 table) — none of that was relevant to a 2023/2025 question, so I removed it and the leaves it fanned out from went out of scope with it. The v2 document's numeric check codes (30–45) are never defined anywhere I found in this working set — I reported the structural change (flat rule → two-qualifier matrix) rather than inventing a meaning for those numbers.
