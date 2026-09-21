1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Team manager, Dhaka, 4 nights - hotel per-night cap and receipt threshold?" --member /v1/regions/expense "trip pay / hotel amounts / receipt requirement likely here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_912e89 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s2/body

2. **Answer**:
Lodging cap: 211 USD per night. Receipt required for any single item above 52 USD (the receipt threshold on this row). This is the current overseas per-diem table, in force from 2026-01-01, so it applies today (2026-09-21).

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body (team manager → grade G2)
/v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
/v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
/v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s2/body (the rates: lodging 211 USD/night, receipt threshold 52 USD)

4. **Notes**:
"Four nights" maps exactly onto the S2 legend entry ("four nights"), so no rounding/nearest-band judgment call was needed there — unlike grade or band, which required no interpretation either since "team manager" and "Dhaka" are both listed verbatim in their legends. The one thing worth flagging: the expense area's table surfaced a loud warning (`hard-perdiem-legend-revision`) that overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`). It would be easy to grab the wrong version if you didn't notice the "in force from 2026-01-01" note on the table listing — I confirmed the row's own footer repeats that same effective date, and today (2026-09-21) falls inside it, so `sec-hard-perdiem` is correct. The overlay's `used` addresses were all reached by drilling into a table member rather than being direct overlay members themselves, which the tool flagged as "reached = answered from somewhere the overlay never named" — that's just the tool's bookkeeping, not an error; the underlying documents are exactly the ones that answer the question.
