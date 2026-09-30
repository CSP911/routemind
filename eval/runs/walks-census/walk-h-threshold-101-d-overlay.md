1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C2, amount V1, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term"
./bench/rmcli.py overlay add --id ov_2026-09-21_029ff1 --address /v1/nodes/sec-hard-threshold --why "current approval threshold table, in force 2026-01-01 onwards, indexed by three qualifiers (category, amount, term) — matches question dated 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_029ff1 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body

2. **Answer**
The team lead signs it off. No competing quotes are required (delegation limit 1,017 thousand KRW; 3 working days to expect).

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three approval-threshold versions applies to today's date, 2026-09-21)
/v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body (the row itself, from the current table `sec-hard-threshold`, in force 2026-01-01 onwards)

4. **Notes**
The approval-threshold subject has three versions in force over different date ranges (`threshold-table` until 2024-07-01, `hard-threshold-v2` 2024-07-01 to 2025-12-31, `sec-hard-threshold` from 2026-01-01), and the legend-revision page warns explicitly that the oldest version says nothing about being superseded and that reaching for the newest is wrong for dates before 2026-01-01. It would have been easy to skip that check and just grab whichever C2/V1/M2 row appeared under `sec-hard-threshold` without confirming the date actually falls in its range — today (2026-09-21) does, but a 2025-dated question would need `hard-threshold-v2` instead, which is indexed by only two qualifiers, not three, so a row address in that shape wouldn't even exist there. Also note: the overlay's initial member (`/v1/regions/procurement`) surfaced a large table of loosely-related procurement pages (vendor registration, contract custody, due diligence, etc.); adding the more specific `/v1/nodes/sec-hard-threshold` member as a second working-set entry was what actually narrowed things down to the right row, since `overlay remove` only works on addresses added as explicit members, not on rows merely displayed under a member's table.
