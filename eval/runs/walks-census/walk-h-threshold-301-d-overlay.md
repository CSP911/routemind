1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C4, amount V1, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold table is keyed by category, amount and term - matches question exactly"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_142625 --outcome answered --used /v1/nodes/sec-hard-threshold/body /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body

2. **Answer**
For category C4, amount V1, term M2: the team lead signs it off. No competing quotes are required ("Competing quotes: none"). Delegation limit is 1,049 thousand KRW, and the expected turnaround is 3 working days.

3. **Source**
- /v1/nodes/sec-hard-threshold/body (table listing this as the current approval threshold table, in force from 2026-01-01)
- /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body (the row itself, used for the answer)

4. **Notes**
- The procurement region table's one-line description ("how far up this amount has to be approved — the approval threshold by category, amount and term") was an exact match for the question, so this was a clean single-hop pick with no real ambiguity.
- Opening /v1/nodes/sec-hard-threshold surfaced a scary-looking warning node, `hard-threshold-legend-revision`, saying the approval threshold has three historical versions. I almost went down that path to double check dates, but `sec-hard-threshold` itself was already explicitly labeled "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01" and today is 2026-09-21, so the current table is the right one and the row itself also states "In force from 2026-01-01" with the prior versions named for reference only. No need to open the legend-revision or v2 files.
- The overlay's row-selection table for /v1/nodes/sec-hard-threshold has 64 rows (one per category/amount/term combination), but since the question gave all three qualifiers (C4, V1, M2) explicitly, the exact row address could be read directly off the listing without needing the three separate legend files (amount/category/term) that translate plain-language qualifiers into codes.
- I read the row and closed the overlay using the two addresses that actually answered the question, but I had never added them as overlay members first (I'd only added the parent /v1/regions/procurement row). The tool flagged this as "reached = answered from somewhere the overlay never named" rather than rejecting it — worth being more disciplined about promoting addresses into the working set as I go, even on short walks.
