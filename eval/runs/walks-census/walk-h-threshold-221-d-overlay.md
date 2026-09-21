1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C3, amount V3, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term, in force since 2026-01-01, matches today's date 2026-09-20" --member /v1/nodes/purchase-request "how many quotes are needed before purchase - covers 'other prices first' question"
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_0329ae --outcome answered --used /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body

2. **Answer**: For category C3, amount V3, term M2: signed off by the department head. Yes — three competing quotes are required before purchase. (Delegation limit: 20,041 thousand KRW; 9 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m2/body

4. **Notes**: The procurement table warns that the approval threshold has had three versions over time, with a legend page (hard-threshold-legend-revision) to sort out which applies when. I didn't need it here because the current table (sec-hard-threshold, in force since 2026-01-01) covers today's date (2026-09-20) with no ambiguity, and the row list under it is already split out per exact category/amount/term combination — the overlay table printed a row named exactly `hard-threshold-row-category-c3-amount-v3-term-m2`, so no interpretation was needed to pick it. I did not end up needing the `purchase-request` member (with its `approval-threshold` table by amount band only, no category/term breakdown) — the per-row page itself already answers "how many quotes" via its "Competing quotes" field, which covers the "other prices first" half of the question directly, so that second member was unused. One procedural note: I read the row address directly rather than adding it to the overlay with `overlay add` first, so the close command reported it as "reached" (answered from an address the overlay never named) rather than as a matched member — functionally fine, but if reproducing this walk, adding the exact row before closing would keep the overlay's own bookkeeping cleaner.
