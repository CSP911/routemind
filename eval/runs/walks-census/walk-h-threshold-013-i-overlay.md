1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A couple of laptops, roughly 3 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "recurring purchase (until cancelled) of laptops ~3M won looks like a term/rental procurement item - need approval threshold and competitive quote requirement"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_838b00 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body

2. **Answer**
The division director signs it off, and yes — two competing quotes are required. (Delegation limit for this row is 5,007 thousand KRW; expect about 8 working days.)

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (laptops → category C1)
- /v1/nodes/hard-threshold-legend-amount/body (roughly 3 million won → amount V2)
- /v1/nodes/hard-threshold-legend-term/body (until we cancel it → term M4)
- /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body (the row itself: division director, two quotes)

4. **Notes**
The table listing under /v1/regions/procurement surfaced both a current threshold table (`sec-hard-threshold`, in force from 2026-01-01) and a superseded one (`hard-threshold-v2`, 2024-07-01 to 2025-12-31), plus a "legend-revision" warning page flagging three total versions. It would have been easy to grab the wrong vintage — I stuck with `sec-hard-threshold` since it's explicitly labeled current and today (2026-09-21, per the environment clock, vs. the 2026-09-20 given in the prompt — both fall inside the 2026-01-01+ window) is well inside its effective range, so the choice didn't actually turn on which date was right.

The three legends (category, amount, term) each say plainly "this is the only place the mapping is written down" and warn to pick the nearest entry if the exact value isn't listed. All three of this question's values happened to match a legend row exactly (laptops=C1, ~3M won=V2, "until we cancel it"=M4), so no judgment call was needed there — but the wording of "until we cancel it" mapping to "term M4" was the one place I paused, since it's phrased as an open-ended/evergreen commitment rather than a fixed renewal cycle; the legend's own phrasing matched verbatim, so I treated that as decisive.

One process wrinkle: I read the legend and row files directly with `read` rather than adding them to the overlay one at a time with `overlay add`. The close command still accepted them as `--used` addresses but flagged them as "reached = answered from somewhere the overlay never named" rather than "used" from a tracked member. The answer is unaffected, but a stricter walk would have `add`ed each legend/row address to the overlay as I opened it, rather than jumping straight to `read`.
