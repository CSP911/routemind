1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/hard-diligence-v2

2. Answer

Supplier due diligence has been written three times, and a 2023 question and a 2025 question land on two different versions — neither the oldest nor the current one alone answers this.

**In 2023** (rule in force until 2024-07-01, uniform for every supplier — no origin or value qualifier): three checks were required before a vendor could be registered —
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen (has this entity or its owners been flagged before)

A sanctions hit or a refused code of conduct stopped registration outright, with no delegated sign-off able to override it, and a hit found after registration was treated the same as one found before — suspension and frozen purchase orders.

**By 2025** (the second version, in force 2024-07-01 to 2025-12-31): the flat three-check rule became a matrix, with the checks required now varying by supplier origin (O1–O4) and contract value band (W1–W4) — a 4x4 table of 16 cells (values 30–45 in the source table, given as bare codes with no decode table reachable from this walk). Everything else — the documents to collect and the re-review interval — continued to follow the original 2023 rule unchanged. (From 2026-01-01 onward a third version adds goods supplied as a further qualifier, but that is out of scope for this question.)

3. Source

/v1/nodes/hard-diligence-legend-revision/body — version index, confirms 2023 → oldest table, 2025 → second version, and that the current table would be wrong for either date
/v1/nodes/supplier-due-diligence/body — the 2023 (pre-2024-07-01) rule, the three checks
/v1/nodes/hard-diligence-v2/body — the 2025 (2024-07-01 to 2025-12-31) rule, the origin×value matrix

4. Notes

The trap here is explicit in the source and easy to fall into anyway: the procurement table's top-level listing surfaces `sec-hard-diligence` as "THE CURRENT SUPPLIER DUE DILIGENCE TABLE" front and center, and it would have been easy to grab that for "2025" since 2025 sounds recent. The legend-revision page is what corrects this — current only applies from 2026-01-01, and 2025 actually belongs to the superseded middle version (hard-diligence-v2), while the current table postdates both dates in the question. The oldest version's address (`supplier-due-diligence`) also isn't listed anywhere in the procurement area's own table — it only turned up one hop further, under `sec-supplier-due-diligence`'s "where to start" listing. Anyone stopping at the procurement table's listing alone (which shows hard-diligence-v2, hard-diligence-legend-revision, and sec-hard-diligence but not the oldest file) could easily conclude the oldest version isn't retrievable and report "not found" for 2023, which would be wrong.

Separately, the 2025 table's cells are bare numeric codes (30–45) against O1–O4 / W1–W4 axes with no decode legend reachable from this walk — I reported the codes and the shape of the matrix as-is rather than guessing what they mean, since the question asked what the screening "had become" structurally, not for a specific origin/value combination.
