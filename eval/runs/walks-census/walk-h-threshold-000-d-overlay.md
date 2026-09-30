1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V1, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term is procurement's exact scope"
./bench/rmcli.py overlay remove --id ov_2026-09-21_2e4569 --address /v1/nodes/contract-custody --why "not about signatures/threshold"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay add --id ov_2026-09-21_2e4569 --address /v1/nodes/sec-hard-threshold --why "current approval threshold table in force 2026-01-01 onwards, matches today's date 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_2e4569 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body

2. **Answer**:
For category C1, amount V1, term M1 (delegation limit 1000 thousand KRW): the team lead signs it off. No competing quotes are required ("Competing quotes: none"). Expect 2 working days. This is under the current threshold table, in force from 2026-01-01 onward.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (established that the current table applies, since today's date 2026-09-21 falls after 2026-01-01)
/v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body (the row with the actual answer)

4. **Notes**:
The question used literal placeholder-style labels ("C1", "V1", "M1") which turned out to be exact qualifier codes used in RouteMind's own indexing scheme, not stand-ins I had to resolve myself — the address `hard-threshold-row-category-c1-amount-v1-term-m1` matched directly. That was a pleasant surprise, but it could easily have gone the other way if the real qualifiers were named differently, so it's worth flagging as a place where a differently-worded question could require a legend lookup (`hard-threshold-legend-category`, `-legend-amount`, `-legend-term`) first to map real-world values to C/V/M codes.

The bigger trap was version handling: there are three superseded versions of the approval-threshold table (`threshold-table` pre-2024-07-01, `hard-threshold-v2` for 2024-07-01–2025-12-31, and `sec-hard-threshold` current from 2026-01-01), and the legend-revision page explicitly warns that reaching for the newest is wrong for any date before 2026-01-01, and that the oldest version says nothing about being replaced. Today's date (2026-09-21) is safely in the current version's range, so `sec-hard-threshold` / the row under it was correct — but I made a point of reading the revision-legend page before trusting the current table, and I'd flag that any question without today's date as an anchor would need that same check.

Also worth noting: `overlay remove` failed with a 404 the first time I tried it — the rows listed after `overlay create` are the rows visible from opening the member address, not overlay members themselves, so nothing was actually "in" the overlay to remove yet. Only `overlay add` on a specific address actually adds it as a member (and then reveals its own child rows). I switched to `add` instead of trying to prune, which worked as expected.
