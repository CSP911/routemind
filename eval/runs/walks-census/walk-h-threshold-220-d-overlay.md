1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C3, amount V3, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term lives here"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/hard-diligence-legend-revision/body --why "diligence, not threshold; irrelevant to signature question"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/hard-diligence-v2/body --why "diligence, not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/hard-threshold-v2/body --why "superseded version (2024-07-01 to 2025-12-31); today is 2026-09-21 so current table applies"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/sec-hard-diligence --why "diligence table, not approval threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/sec-supplier-due-diligence --why "diligence, not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/sec-vendor-performance-and-renewal --why "not relevant"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/sec-receiving-and-inspection --why "not relevant"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/vendor --why "not relevant"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/sec-contract-terms-the-company-insists-on --why "not relevant to signature/quotes question"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/contract-custody --why "not relevant"
./bench/rmcli.py overlay remove --id ov_2026-09-21_9a4dfc --address /v1/nodes/ga-desk --why "not relevant"
./bench/rmcli.py table /v1/overlays/ov_2026-09-21_9a4dfc
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_9a4dfc --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body

2. **Answer**:
Signs it off: the department head.
Competing quotes required: three (so yes, other prices are required first).
Delegation limit for this row: 20,040 thousand KRW. Working days to expect: 8.

3. **Source** (in order used):
- /v1/nodes/hard-threshold-legend-revision/body — confirmed which of the three approval-threshold table versions is current for today's date (2026-09-21 falls in the "2026-01-01 onwards" version, `sec-hard-threshold`)
- /v1/nodes/sec-hard-threshold — the current approval threshold table, listing the row for category C3, amount V3, term M1
- /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m1/body — the row itself, giving the signer and quote requirement

4. **Notes**:
There are three separate versions of this approval-threshold document (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-21) is safely inside the current version's range, so this wasn't a hard call here, but it would be easy to skip the legend check and grab the wrong version for a question dated in 2025 — the table under `/v1/regions/procurement` surfaces the current, the v2, and the legend-revision file side by side with only a truncated one-line description to tell them apart, so slowing down to read the legend page in full was necessary rather than optional.

The `overlay remove` calls all failed with HTTP 404 ("not in this overlay"), even though the addresses were exactly as printed in the overlay's own creation output. I couldn't determine why (possibly the create call didn't actually persist non-`--member` rows as removable members, or the printed table included rows adjacent to the overlay rather than strictly inside it). This didn't block the answer — I read the exact row directly once I found it listed under `/v1/nodes/sec-hard-threshold` — but it meant the working set I tried to maintain never actually narrowed, and `overlay close` reported all three "used" addresses as "reached ... from somewhere the overlay never named" rather than as formal overlay members. Worth flagging: the overlay add/remove mechanics didn't behave as documented in this run.

The three-qualifier row address pattern (`hard-threshold-row-category-c3-amount-v3-term-m1`) was fully enumerated in the `sec-hard-threshold` table listing, so once that table was open the exact row for C3/V3/M1 was a direct pick — no ambiguity there.
