1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "MD, Jakarta, 3 weeks: nightly hotel cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, since 2026-01-01" --member /v1/nodes/evidence "receipt requirement threshold" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of 3 versions with different dates - need to confirm which applies today"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-evidence/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_b605c2 --address /v1/nodes/qualified-evidence --why "domestic KRW simple-receipt rule, not the overseas per-diem receipt threshold; distractor"
./bench/rmcli.py overlay close --id ov_2026-09-21_b605c2 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body

2. **Answer**:
Nightly hotel (lodging) cap: 331 USD per night.
Receipt required above: 57 USD (the receipt threshold for this row). Below that, no receipt is required for this line.
(For reference, same row also gives meals at 108 USD/day and incidentals at 22 USD/day, not asked for but on the same row.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem table versions is in force for today's date, 2026-09-21 — the current one, since 2026-01-01)
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → band B3)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → stay S4)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s4/body (the answer: lodging 331 USD/night, receipt threshold 57 USD)

4. **Notes**:
The per-diem table is indexed by three qualifiers (grade, band, stay) that each have to be looked up separately in their own legend documents before the row address can be built — the row isn't guessable from the question's plain-language inputs ("managing director", "Jakarta", "three weeks"), it has to be translated through G4/B3/S4 first.
The real trap here was the version warning: /v1/nodes/hard-perdiem-legend-revision/body was explicit that there are three per-diem tables covering different date ranges and that reaching for the newest one is wrong for anything before 2026-01-01. Since today is 2026-09-21, the current table (`sec-hard-perdiem`) is correct, but I checked the warning deliberately rather than assuming — the region table itself listed `hard-perdiem-v2` right next to the current table with almost identical wording ("SUPERSEDED"), and it would have been easy to grab the wrong one without reading the legend first.
I also went down a side path on "receipt threshold": the expense region's `/v1/nodes/evidence` table led to `/v1/nodes/qualified-evidence`, a general evidence-qualification rule stated in KRW (a 30,000 KRW simple-receipt ceiling) for domestic-style claims. That is a different rule from the per-diem row's own "Receipt threshold" field (57 USD), which is specific to this overseas per-diem line. I nearly conflated the two — they answer superficially similar-sounding questions ("above what amount do I need a receipt") but apply to different expense types and currencies. The per-diem row's own field is the one that actually answers this question since it's an overseas hotel/per-diem context, so I used that and excluded the KRW general-evidence rule as a distractor.
