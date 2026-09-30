1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G4, band B2, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force from 2026-01-01, likely has hotel nightly cap" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of three versions of the per-diem table with different dates, need to confirm which applies now" --member /v1/nodes/evidence "evidence/receipt rules - may state the amount above which a receipt must be kept"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_ab432b --address /v1/nodes/hard-perdiem-legend-revision/body --why "row itself states its own in-force dates (2026-01-01 onward), which cover today 2026-09-21; no need for the separate version legend"
./bench/rmcli.py overlay remove --id ov_2026-09-21_ab432b --address /v1/nodes/evidence --why "the per-diem row already gives its own receipt threshold (48 USD) inline; general evidence table not needed"
./bench/rmcli.py overlay close --id ov_2026-09-21_ab432b --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body
```

2. **Answer**
Lodging (hotel), per night: 315 USD. Receipt must be kept above 48 USD.
(For context, also on this row: meals 94 USD/day, incidentals 19 USD/day — not asked, not reported as the answer, just noted here.)

3. **Source**
- `/v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s4/body` — the current (in force from 2026-01-01) overseas per-diem row for grade G4, band B2, stay S4.

4. **Notes**
- The `/v1/regions/expense` table flags upfront that overseas per-diem has THREE versions with different dates (current, `hard-perdiem-v2` for 2024-07-01–2025-12-31, and an older `overseas-rates`). I pulled in the version-legend doc as a safety member expecting I'd need to cross-check which one applies to today (2026-09-21). It turned out unnecessary: the row itself states "In force from 2026-01-01" directly under the figures, which already covers today, so I removed the legend doc from the working set rather than read it. Worth flagging because it would be an easy place to grab the wrong table if working faster and skipping that in-force line.
- I also pre-loaded the general `evidence` table (`qualified-evidence`) expecting the receipt-threshold figure might live there instead of in the per-diem row. It didn't need to — the per-diem row carries its own "Receipt threshold" field (48 USD) specific to this grade/band/stay combination, so that's the correct number to use, not a general evidence-table figure. Good thing I checked the row first before assuming I'd need the general evidence table.
- The overlay's `close` output labeled the used address as "reached" rather than a plain match, with the note "answered from somewhere the overlay never named." This is because by the time I closed, I had removed the other two safety members but the G4/B2/S4 row itself was always present in the overlay (it came from the `/v1/nodes/sec-hard-perdiem` table expansion, not one I added directly) — a slightly confusing bit of bookkeeping but the address used is correct and exact as printed.
