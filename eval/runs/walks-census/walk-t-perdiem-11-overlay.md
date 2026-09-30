1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Nightly lodging cap for band B destination overseas per-diem 2023 vs 2025" --member /v1/regions/expense "expense table covers business trip pay including per-diem/lodging caps"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py overlay add --id ov_2026-09-20_9cfc8f --address /v1/nodes/overseas-rates/body --why "oldest version, in force until 2024-07-01, covers 2023 question date"
./bench/rmcli.py overlay remove --id ov_2026-09-20_9cfc8f --address /v1/nodes/sec-hard-perdiem --why "current table only covers 2026-01-01 onward, not needed for 2023/2025 dates"
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py overlay add --id ov_2026-09-20_9cfc8f --address /v1/nodes/sec-hard-perdiem --why "check current 3-qualifier structure to understand what v2's B1-B4 columns mean"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9cfc8f --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/overseas-rates/body /v1/nodes/hard-perdiem-v2/body /v1/nodes/hard-perdiem-legend-band/body

2. **Answer**:
- 2023 (in force until 2024-07-01, under `overseas-rates`): Band B (China, South-East Asia, Eastern Europe) nightly lodging cap = **USD 180**. This is a single flat figure with no grade dependency.
- 2025 (in force 2024-07-01 to 2025-12-31, under `hard-perdiem-v2`): There is no single "Band B" figure anymore. The letter-band scheme (A/B/C by broad region) was retired and replaced by a grade × numbered-band table, where "band" now means one of four city-indexed tiers B1–B4 (Tokyo=B1, Singapore=B2, Jakarta=B3, Dhaka=B4 — mapped by nearest match for unlisted cities), crossed with grade G1–G4. Old Band-B destinations don't land on one new code: e.g. Singapore (old Band B) is now B2, Jakarta (old Band B) is now B3. Across the whole v2 table the nightly lodging cap ranges from USD 95 (G1/B1) to USD 155 (G4/B4); for the B2/B3 columns specifically (the closest successors to old Band B) it runs USD 99–147 depending on grade. There is no single number that is "the 2025 version of the USD 180 Band B cap" without also knowing the traveler's grade and which specific city/numbered band applies.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established which of the three versions covers which date range)
- /v1/nodes/overseas-rates/body (2023 figure: Band B lodging cap = USD 180)
- /v1/nodes/hard-perdiem-v2/body (2025 figures: grade × B1–B4 lodging cap table)
- /v1/nodes/hard-perdiem-legend-band/body (confirmed B1–B4 are city-indexed tiers, not a renumbering of the old A/B/C region letters)

4. **Notes**:
- The overseas per-diem subject has three non-overlapping versions and the oldest one (`overseas-rates`) never says it was superseded — you have to find `hard-perdiem-legend-revision` first or you'll silently answer 2025 questions from a 2026-onward table (`sec-hard-perdiem`) or a pre-2024-07-01 table, both wrong.
- The real trap here is the word "band" itself, not the version-dating. In the 2023 rule, "Band B" is a letter naming one of three broad region groups (A/B/C). In the 2024-07-01–2025-12-31 rule, the table's column headers are also "B1/B2/B3/B4" — sharing the letter B — but that B is short for the word "Band" (the axis name), the same way grades are G1–G4 and stay lengths are S1–S4. It is not a continuation of the old region-letter B. I nearly reported the v2 table's "B" columns as-is as "the 2025 version of Band B," which would have been a false match on the letter alone. Checking `hard-perdiem-legend-band` (which maps individual cities to B1–B4) showed old Band-B cities scatter across B2 and B3, not one code — so there is no clean single 2025 figure, and I've reported the range instead of picking one column that only coincidentally shares a letter with the 2023 term.
- Minor procedural snag: removing `/v1/nodes/sec-hard-perdiem` from the overlay failed with a 404 ("not in this overlay") because it had only ever appeared as part of the `/v1/regions/expense` group, not as an individually-added member — harmless, but worth noting the remove op only works on rows added via `add`.
