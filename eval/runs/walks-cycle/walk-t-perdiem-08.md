1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body

2. **Answer**
For a claim dated anywhere in 2025, the applicable overseas per-diem version is the *second* version, "Overseas per-diem, second version," in force 2024-07-01 to 2025-12-31 (not the oldest pre-2024-07-01 rule, and not the current table that starts 2026-01-01).

Its nightly lodging cap, by grade and destination band:

| grade \ band | B1 | B2 | B3 | B4 |
|---|---|---|---|---|
| G1 | 95 USD | 99 USD | 103 USD | 107 USD |
| G2 | 111 USD | 115 USD | 119 USD | 123 USD |
| G3 | 127 USD | 131 USD | 135 USD | 139 USD |
| G4 | 143 USD | 147 USD | 151 USD | 155 USD |

The daily meal allowance and the receipt threshold were not changed in this version — they still follow the older "overseas allowance and exchange rate" rule (address `/v1/nodes/overseas-rates`) unchanged until 2026-01-01. This version added stay was not yet a qualifier (that comes in the 2026-01-01 table, which adds a third qualifier).

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (which version covers which date range)
- /v1/nodes/hard-perdiem-v2/body (the actual 2024-07-01–2025-12-31 figures)

4. **Notes**
The expense area table lists three per-diem-looking entries side by side: `hard-perdiem-legend-revision`, `hard-perdiem-v2`, and `sec-hard-perdiem` (the current one, flagged "CURRENT" in the row description). It would be easy to grab `sec-hard-perdiem` on reflex since it's marked current and sits lower in the list looking authoritative — that would have been wrong for a 2025-dated claim. The legend/revision document exists specifically to catch this and says so explicitly: "reaching for the newest is wrong for anything before 2026-01-01." It also warns the oldest version (`overseas-rates`) never mentions being superseded, so without the legend doc there'd be no way to know three versions even exist. I did not fetch `/v1/nodes/overseas-rates` itself since the meal-allowance/receipt-threshold figures weren't asked for and hard-perdiem-v2 already states plainly that those followed the old rule unchanged — that address is named here only as a pointer, not verified by reading it.
