1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Team manager, Dhaka, three weeks: hotel per-night cap and receipt threshold?" --member /v1/regions/expense "business trip hotel spend and receipt rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py overlay add --id ov_2026-09-21_c66c76 --address /v1/nodes/hard-perdiem-legend-grade/body --why "need grade code for a team manager"
./bench/rmcli.py overlay add --id ov_2026-09-21_c66c76 --address /v1/nodes/hard-perdiem-legend-band/body --why "need band code for Dhaka"
./bench/rmcli.py overlay add --id ov_2026-09-21_c66c76 --address /v1/nodes/hard-perdiem-legend-stay/body --why "need stay code for three weeks"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_c66c76 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body

2. **Answer**: Lodging cap is 219 USD per night. The receipt threshold is 58 USD — spend above that amount requires a receipt to be kept/attached (per this row of the current overseas per-diem table, in force from 2026-01-01).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies for a 2026-09-21 question — the current one)
- /v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body (the answer: 219 USD lodging/night, 58 USD receipt threshold)

4. **Notes**: The per-diem subject has three superseded/current versions of the same table (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the warning page explicitly says the oldest version doesn't mention being replaced, so it's easy to grab the wrong one if you don't check dates first. Today's date (2026-09-21) falls after the 2026-01-01 cutover, so the current table `sec-hard-perdiem` was correct, but I deliberately read the revision-legend before opening any row to avoid quoting a superseded rate. The three qualifiers (grade, band, stay) each needed their own legend lookup since the row addresses are keyed by code, not by the plain-language terms in the question — "three weeks" happened to map exactly to "stay S4" with no interpolation needed, and Dhaka was listed explicitly as band B4, so no nearest-neighbor guessing was required here. The overlay close command reported the revision-legend and the final row as "reached ... from somewhere the overlay never named" rather than "member" — this is because I read the revision-legend before formally adding it as an overlay member (it was already in the initial working set from the /v1/regions/expense create) and the row address itself was never added as a member, only browsed via the sec-hard-perdiem table listing. Worth noting but didn't affect the answer.
