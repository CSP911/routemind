1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body

2. **Answer**
Overseas per-diem has three written versions, indexed by date. A claim dated anywhere in 2025 falls in the second version, in force 2024-07-01 to 2025-12-31 — not the oldest ("overseas allowance and exchange rate") and not the current table (in force from 2026-01-01). The nightly lodging cap under that 2025-applicable version, by grade and destination band:

| grade \ band | B1 | B2 | B3 | B4 |
|---|---|---|---|---|
| G1 | 95 USD | 99 USD | 103 USD | 107 USD |
| G2 | 111 USD | 115 USD | 119 USD | 123 USD |
| G3 | 127 USD | 131 USD | 135 USD | 139 USD |
| G4 | 143 USD | 147 USD | 151 USD | 155 USD |

The other figures (daily meal allowance, receipt threshold) were not varied in this version and follow the older "overseas allowance and exchange rate" rule unchanged until 2026-01-01.

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-v2/body

4. **Notes**
The expense area table lists three separate per-diem-related entries side by side (the legend/revision doc, the v2 doc, and the current `sec-hard-perdiem` table), with no obvious sort order pointing to "the one to read first." It would be easy to grab `sec-hard-perdiem` directly since it's flagged "THE CURRENT OVERSEAS PER-DIEM TABLE" and skip the date check entirely — that table only applies from 2026-01-01 and would have been the wrong answer for a 2025 claim. The legend doc at `hard-perdiem-legend-revision` exists specifically to prevent that mistake: it states plainly that reaching for the newest table is wrong for anything before 2026-01-01, and that the oldest version says nothing about having been superseded, so date-checking can't be skipped. Reading the legend first before picking a version was the right call and avoided the trap.
