1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For something dated 3 July 2024 (two days after the first change), what was the nightly lodging cap for a grade 2 traveller going to a band B2 destination? Use the version in force on that day." --member /v1/regions/expense "lodging cap by grade and destination band is a travel/expense policy matter"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_16a20f --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-v2/body

2. **Answer**: 115 USD per night.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (to identify which of the three per-diem versions covers 2024-07-03)
- /v1/nodes/hard-perdiem-v2/body (the G2/B2 nightly lodging cap table)

4. **Notes**: The legend document was the key to not going wrong here — this subject has three separately-written versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onwards), and the legend warns explicitly that reaching for the current/newest table is wrong for any date before 2026. "The first change" in the question is the transition from the old `overseas-rates` rule to `hard-perdiem-v2` on 2024-07-01; 3 July 2024 is two days after that, still inside the v2 window (2024-07-01 to 2025-12-31), so v2 is the correct version — not the oldest rule and not the current (2026) table. The v2 document itself restates its own effective range, which corroborated the legend's dating rather than contradicting it. Straightforward once the legend page was read first; would have been easy to grab the current `sec-hard-perdiem` table by mistake since it's the one prominently labeled "current."
