1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Reconciling claims from 2023 and 2025 against approval threshold - which two versions needed, delegation limit or signer under each?" --member /v1/nodes/hard-threshold-legend-revision/body "explains which version covers which date range" --member /v1/nodes/hard-threshold-v2/body "version in force 2024-07-01 to 2025-12-31, likely covers 2025 claim" --member /v1/nodes/sec-hard-threshold "current table in force from 2026-01-01, need to check if it covers any part of question"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/nodes/approval-line
./bench/rmcli.py table /v1/nodes/delegated-approval
./bench/rmcli.py read /v1/nodes/delegation-scope/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/sec-the-approval-behind-a-purchase
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py read /v1/nodes/threshold-table/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_9a8aa4 --address /v1/nodes/sec-hard-threshold --why "current table, in force only from 2026-01-01, does not cover 2023 or 2025"
./bench/rmcli.py overlay add --id ov_2026-09-20_9a8aa4 --address /v1/nodes/threshold-table/body --why "the oldest approval-threshold version, in force until 2024-07-01, covers the 2023 claim"
./bench/rmcli.py overlay close --id ov_2026-09-20_9a8aa4 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/threshold-table/body /v1/nodes/hard-threshold-v2/body

2. Answer
Two versions of the approval threshold apply, split at 2024-07-01:

For the 2023 claim — the oldest version, in force until 2024-07-01 (`threshold-table`), indexed by amount only. Delegation limit / who signs:
- Under 500,000 KRW (net of VAT): Team lead, delegated — 1 quote
- 500,000 – 3,000,000 KRW: Division head, delegated — 2 quotes
- 3,000,000 – 10,000,000 KRW: CEO — 3 quotes
- 10,000,000 KRW and over: CEO, with a separate proposal — 3 quotes plus a comparison
(The document itself notes: "The authority itself is set by the delegation rules — this table is that authority applied to purchasing.")

For the 2025 claim — the second version, in force 2024-07-01 to 2025-12-31 (`hard-threshold-v2`), indexed by category and amount (no term yet). Threshold amounts by category/amount band:
- C1: V1 1,000 / V2 5,001 / V3 20,002 / V4 100,003 (thousand KRW)
- C2: V1 1,004 / V2 5,005 / V3 20,006 / V4 100,007 (thousand KRW)
- C3: V1 1,008 / V2 5,009 / V3 20,010 / V4 100,011 (thousand KRW)
- C4: V1 1,012 / V2 5,013 / V3 20,014 / V4 100,015 (thousand KRW)
Who signs each band, quote counts, and turnaround time were unchanged from the prior rule for this version — this document only re-bands the amounts, it does not itself name signers per band.

3. Source
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/threshold-table/body
/v1/nodes/hard-threshold-v2/body

4. Notes
The trap here was the address for the pre-2024-07-01 version. Both the legend-revision page and the hard-threshold-v2 page name it only as `threshold-table` — a bare id, not a full address — and it does not appear anywhere in /v1/regions/procurement's own table listing (which only surfaces hard-threshold-v2, sec-hard-threshold, and the legend-revision page). I initially suspected it might be the same thing as the approval region's `delegation-scope` page ("Scope by authority", same KRW figures: <500,000 / <3,000,000 / >=3,000,000), since the question's wording "delegation limit" matches that page's language closely and /v1/nodes/hard-moved-threshold/body explicitly calls delegation-scope "the old rule, correct only before 2026-01-01." But delegation-scope is described as valid for the whole span before 2026-01-01 with no 2024-07-01 break, whereas the procurement lineage explicitly breaks at 2024-07-01 — two different systems that happen to share numbers because one is built on the other ("this table is that authority applied to purchasing"). Taking delegation-scope as the 2023 answer would have collapsed the two-version structure the question is asking about into one, so I kept looking. The actual `threshold-table` address only turned up three hops later, off a branch under /v1/nodes/purchase-request → /v1/nodes/approval-threshold — not reachable in the obvious top-down path through procurement. If I'd stopped after not finding it in the procurement table, I'd have wrongly reported "not found" for the 2023 half.
