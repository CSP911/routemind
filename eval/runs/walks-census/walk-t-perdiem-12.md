1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body

2. **Answer**:
Two versions are needed: the oldest overseas allowance table (covers the 2023 claim, in force until 2024-07-01) and the second version, "Overseas per-diem" v2 (covers the 2025 claim, in force 2024-07-01 to 2025-12-31). The current table (`sec-hard-perdiem`, from 2026-01-01) does not apply to either claim.

- **2023 claim** — oldest version (`overseas-rates`), nightly lodging cap by region band only:
  - Band A (US, Western Europe, Japan): USD 250
  - Band B (China, South-East Asia, Eastern Europe): USD 180
  - Band C (Elsewhere): USD 150

- **2025 claim** — v2 (`hard-perdiem-v2`), nightly lodging cap by grade × band:
  | grade \ band | B1 | B2 | B3 | B4 |
  |---|---|---|---|---|
  | G1 | 95 USD | 99 USD | 103 USD | 107 USD |
  | G2 | 111 USD | 115 USD | 119 USD | 123 USD |
  | G3 | 127 USD | 131 USD | 135 USD | 139 USD |
  | G4 | 143 USD | 147 USD | 151 USD | 155 USD |

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (to identify which version covers which date range)
- /v1/nodes/overseas-rates/body (2023 figures)
- /v1/nodes/hard-perdiem-v2/body (2025 figures)

4. **Notes**:
- The region table's own description for /v1/regions/expense already warns "the older band-only caps are still here and are superseded" — that phrase alone would tempt someone into assuming there's only one old version plus the current one. The legend-revision doc was what clarified there are actually three versions, and that 2025 needs the *middle* one, not the oldest and not current — reaching for the current table (`sec-hard-perdiem`, tempting since it's the one flagged "current" everywhere) would have been wrong for both 2023 and 2025.
- Finding the oldest version's real address took an extra hop: `hard-perdiem-legend-revision` names it only as `overseas-rates`, which isn't a full address and isn't listed directly under `/v1/regions/expense`'s table — it's nested one level deeper under `/v1/nodes/travel-expense` → `/v1/nodes/travel-overseas`. Following the "never construct an address" rule literally requires that detour.
- The `hard-perdiem-v2` document contains an internal contradiction worth flagging: it prints an explicit table titled "The nightly lodging cap, by grade and band" with values 95–155 USD, but then a trailing paragraph says "the nightly lodging cap, the daily meal allowance and the receipt threshold beyond the column above followed the overseas allowance and exchange rate rule unchanged until 2026-01-01" — which, read literally, claims the lodging cap did NOT change from the old band-only figures. I went with the explicit table as authoritative (it's also consistent with the legend-revision doc's claim that v2 is "indexed by two qualifiers," i.e. grade and band), but the prose sentence is genuinely ambiguous and someone skimming only the text (not the table) could report the wrong figures.
