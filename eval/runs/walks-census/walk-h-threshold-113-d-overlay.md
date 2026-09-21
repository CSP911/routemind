1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C2, amount V2, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term is the procurement table's stated purpose"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/contract-custody --why "not about approval signature threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/ga-desk --why "not about approval signature threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/hard-diligence-legend-revision/body --why "diligence versions, not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/hard-diligence-v2/body --why "diligence versions, not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/purchase-request --why "process how-to, not the threshold table itself"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/sec-contract-terms-the-company-insists-on --why "contract terms, not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/sec-hard-diligence --why "diligence table, not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/sec-receiving-and-inspection --why "receiving, not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/sec-supplier-due-diligence --why "diligence overview, not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/sec-vendor-performance-and-renewal --why "vendor performance, not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_57b40b --address /v1/nodes/vendor --why "vendor registration, not threshold"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_57b40b --outcome answered --used /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body

2. **Answer**:
For category C2, amount V2, term M4: the division director signs it off. Two competing quotes are required before the purchase (delegation limit is 5023 thousand KRW; 8 working days to expect).

3. **Source**:
/v1/nodes/sec-hard-threshold (table, located the C2/V2/M4 row)
/v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body (the row itself, source of the figures)

4. **Notes**:
The overlay's displayed "15 rows" after `overlay create` turned out to be an expansion of the procurement region table's contents for browsing, not actual overlay members — every `overlay remove` I attempted against those addresses came back 404 "not in this overlay." The only real member was `/v1/regions/procurement` itself. This cost 11 wasted commands but didn't block the answer; worth knowing for next time that overlay create's table listing is informational, not a member roster you can prune item by item.

The current threshold table (`sec-hard-threshold`, in force from 2026-01-01) is the third of three versions — a legend-revision node (`hard-threshold-legend-revision`) and a superseded version (`hard-threshold-v2`, 2024-07-01 to 2025-12-31) both appeared alongside it in the procurement listing. Today's date (2026-09-21) is well inside the current table's validity window, so there was no real ambiguity about which version applies, but it would have been easy to grab the superseded `hard-threshold-v2` row by category/amount/term match alone without checking the effective-date banner. The row itself also carries its own "if the figures are exceeded" clause (unapproved excess is non-recoverable; unavoidable excess needs a written statement decided by the budget holder) — not asked for here, but adjacent enough that it's worth flagging in case it's the next question.
