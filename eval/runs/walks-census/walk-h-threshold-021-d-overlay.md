1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V3, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term matches the question directly"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_a28546 --outcome answered --used /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**:
The department head signs it off. Yes — three competing quotes are required before this can be approved. (Delegation limit for this row is 20,009 thousand KRW; working days to expect: 9.)

3. **Source**:
- /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body (the row itself: signer, quotes, delegation limit)
- /v1/nodes/hard-threshold-legend-revision/body (confirms this current table, in force 2026-01-01 onward, is the correct version for an undated/current-day question rather than the superseded `hard-threshold-v2` or `threshold-table`)

4. **Notes**:
The procurement region table surfaced two near-duplicate rows for approval thresholds — `hard-threshold-v2` (marked SUPERSEDED, in force 2024-07-01 to 2025-12-31) and `sec-hard-threshold` (current, in force 2026-01-01 onward) — plus a `hard-threshold-legend-revision` warning that there are actually three historical versions total. It would have been easy to grab the first threshold-looking row without checking which version is current. Since the question carries no date, I treated it as asked "now" (2026-09-21), which the legend-revision page confirms falls under the current table (`sec-hard-threshold`), not the superseded v2. Worth flagging: the overlay close command reported the two addresses I used as "reached" rather than proper members, because I never ran `overlay add` for them after opening the table — I went straight from `table` to `read` without registering the intermediate hops in the overlay. The answer itself is unambiguous once the correct row is found: the row text names the signer and the quote count plainly, no interpretation needed.
