1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Reconciling 2023 and 2025 overseas per-diem claims: which versions apply and what were the nightly lodging caps?" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of three per-diem versions and which dates each covers" --member /v1/nodes/hard-perdiem-v2/body "version in force 2024-07-01 to 2025-12-31, would cover the 2025 claims" --member /v1/nodes/sec-hard-perdiem "current table from 2026-01-01, for context/exclusion since neither claim year falls here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py overlay add --id ov_2026-09-20_7a87f0 --address /v1/nodes/overseas-rates/body --why "oldest version, in force until 2024-07-01, covers the 2023 claims"
./bench/rmcli.py overlay remove --id ov_2026-09-20_7a87f0 --address /v1/nodes/sec-hard-perdiem --why "current table from 2026-01-01 does not cover either 2023 or 2025 claims"
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7a87f0 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/overseas-rates/body /v1/nodes/hard-perdiem-v2/body

2. **Answer**:
For 2023 claims, use "Overseas allowance and exchange rate" (the oldest version, in force until 2024-07-01). Its nightly lodging cap is by region band only (no grade, no stay length): Band A (US, Western Europe, Japan) USD 250; Band B (China, South-East Asia, Eastern Europe) USD 180; Band C (elsewhere) USD 150.

For 2025 claims, use "Overseas per-diem, second version" (in force 2024-07-01 to 2025-12-31). Its nightly lodging cap is by grade and band (no stay-length qualifier yet):
| grade \ band | B1 | B2 | B3 | B4 |
|---|---|---|---|---|
| G1 | 95 USD | 99 USD | 103 USD | 107 USD |
| G2 | 111 USD | 115 USD | 119 USD | 123 USD |
| G3 | 127 USD | 131 USD | 135 USD | 139 USD |
| G4 | 143 USD | 147 USD | 151 USD | 155 USD |

Note the two versions' bands are not the same scheme (three lettered region bands in the 2023 version vs. four numbered bands crossed with four grades in the 2025 version), so figures don't line up row-for-row.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (identified which of the three versions covers 2023 vs. 2025)
- /v1/nodes/overseas-rates/body (2023 lodging caps, by region band)
- /v1/nodes/hard-perdiem-v2/body (2025 lodging caps, by grade and band)

4. **Notes**:
The current per-diem table (sec-hard-perdiem) is the one that surfaces first and loudest when opening the expense area — it's the top overseas per-diem hit and, being current, is tempting to reach for by default. It would have been wrong for both 2023 and 2025: it only took effect 2026-01-01 and additionally keys on stay-length (grade × band × stay), which neither older version does. The legend-revision doc exists specifically to head this off — it says outright that "reaching for the newest is wrong for anything before 2026-01-01" and calls out 2025 as the case where taking either extreme (oldest or current) is wrong. Worth flagging: the oldest version (overseas-rates) does not itself say it was ever superseded — nothing in that document points forward — so without deliberately going through the legend-revision doc first, someone reconciling a 2023 claim might not even suspect there's a newer scheme to worry about, or might not realize their doc is the historically correct one rather than something a search just happened to surface. Also worth noting: the two versions' lodging caps are structured completely differently (band-only vs. grade-by-band), so "the lodging cap" isn't a single comparable number across the two years — I reported both full tables rather than picking one row, since the question didn't specify a grade or destination.
