1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C1, amount V4, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term, in force since 2026-01-01" --member /v1/nodes/hard-threshold-legend-revision "warns threshold table has three versions - need to confirm which applies for today's date"
./bench/rmcli.py overlay remove --id ov_2026-09-21_618779 --address /v1/nodes/hard-threshold-legend-revision --why "wrong address, missing /body suffix"
./bench/rmcli.py overlay add --id ov_2026-09-21_618779 --address /v1/nodes/hard-threshold-legend-revision/body --why "confirm which threshold table version applies for today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_618779 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m2/body

2. **Answer**:
Signature: the division director signs it off.
Other prices first: yes — three competing quotes and a written comparison are required.
(Also on file: delegation limit is 100,013 thousand KRW; 12 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed 2026-09-21 falls under the current, 2026-01-01-onward table)
/v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m2/body (the answer itself)

4. **Notes**:
- The procurement region table warns up front that the approval-threshold subject has three superseded/current versions, and lists two of them (`hard-threshold-v2`, superseded) alongside the current `sec-hard-threshold` — easy to grab the wrong one if you don't stop to check dates. I deliberately pulled `hard-threshold-legend-revision/body` and read it before trusting `sec-hard-threshold`, since the row itself doesn't say "current," it just says "in force from 2026-01-01" — you have to already know today's date is inside that range to trust it.
- Minor self-inflicted stumble: when creating the overlay I passed `/v1/nodes/hard-threshold-legend-revision` as the member address, copying it from the procurement table listing without the `/body` suffix that the same listing actually printed for that row (kind `file`). The overlay silently accepted the bad address and showed "(nothing here)" under it rather than erroring, which is what tipped me off — I had to remove and re-add with the correct `/body` address. Lesson: always copy the exact printed address, not a shortened version.
- The specific row `/v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m2/body` was never an explicit overlay member — it appeared automatically as a child row under the `sec-hard-threshold` table member, and the close command flagged it as "reached" (answered from somewhere the overlay never named) rather than a named member. Cosmetic, not a correctness issue, but worth knowing: table members expand to show their full row set, and picking a row from that expansion doesn't count as "adding" it.
- No ambiguity in the C1/V4/M2 mapping itself — the question specified all three qualifiers directly, so no need to consult the amount/category/term legends to derive the bands.
