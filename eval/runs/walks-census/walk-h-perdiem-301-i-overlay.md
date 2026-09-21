1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "MD, Tokyo, 4 nights: hotel nightly cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel nightly cap" --member /v1/nodes/hard-perdiem-legend-revision "warns which per-diem version applies to which dates - need to confirm current version applies" --member /v1/nodes/evidence "evidence table likely states the receipt threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_a32306 --address /v1/nodes/hard-perdiem-legend-revision --why "wrong address, missing /body suffix as printed"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay add --id ov_2026-09-21_a32306 --address /v1/nodes/hard-perdiem-legend-revision/body --why "confirms 2026-01-01+ dates use sec-hard-perdiem, the table already selected"
./bench/rmcli.py overlay remove --id ov_2026-09-21_a32306 --address /v1/nodes/sec-evidence-in-awkward-cases --why "not needed - awkward-case evidence rules don't apply here"
./bench/rmcli.py overlay remove --id ov_2026-09-21_a32306 --address /v1/nodes/qualified-evidence/body --why "index page only, the actual content is in qualified-list"
./bench/rmcli.py overlay close --id ov_2026-09-21_a32306 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/qualified-list/body
```

2. **Answer**
Lodging cap: **291 USD per night** (grade G4 = managing director, band B1 = Tokyo, stay S2 = four nights). Over 4 nights that is up to 1,164 USD total, each night capped at 291 USD.
Receipt threshold: keep the receipt for anything **above 33 USD**. (An unrelated, general "simple receipt" rule elsewhere in Expenses uses a 30,000 KRW threshold, but that governs domestic/general evidence, not this overseas per-diem row — the per-diem row's own 33 USD figure is the one that answers this question.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → band B1)
- /v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s2/body (291 USD lodging/night, 33 USD receipt threshold)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms the 2026-01-01-onward table, sec-hard-perdiem, is the one in force for today's date, 2026-09-21)

4. **Notes**
- The per-diem row is indexed by three separate qualifiers (grade, band, stay) each resolved through its own legend page — none of the three is guessable, and the legends explicitly warn the rows "do not repeat what is in the left," so skipping any one of the three legends would have left me guessing at the address to read.
- I made one address mistake: I added `/v1/nodes/hard-perdiem-legend-revision` (no `/body`) as an overlay member, copying it from the region table's "WHY" text rather than the printed address column, and the overlay silently showed "(nothing here)" for it instead of erroring. Caught it, removed it, and re-added the address exactly as printed (`.../body`). Worth flagging: a bad address didn't fail loudly, it just came back empty — easy to miss if you're not checking each member's contents.
- The real trap was the 30,000 KRW "simple receipt" ceiling in `/v1/nodes/qualified-list`, which sits in the same Expense area and answers a very similar-sounding question ("above what amount do I need a real receipt") but in the wrong currency and for a different scope — general/domestic evidence rules, not this overseas per-diem line. I read it, considered using it, and rejected it because the per-diem row itself already carries its own "Receipt threshold: 33 USD" figure specific to this claim. Using the KRW figure instead would have been a plausible-looking wrong answer.
- Confirmed via `hard-perdiem-legend-revision` that today's date (2026-09-21) falls under the current (2026-01-01-onward) table, `sec-hard-perdiem` — the one I already used — so no version-mismatch risk here, but this is exactly the kind of question where reaching for the newest table without checking dates would have been wrong for a differently-dated question.
- Two overlay `remove` calls at the end (for `sec-evidence-in-awkward-cases` and `qualified-evidence/body`) errored with HTTP 404 "not in this overlay" — those were child rows shown under a table member, not members themselves, so they couldn't be removed directly. Harmless, but the overlay close output labeled several used addresses "reached" (answered from somewhere not formally named as a member) rather than "member" — cosmetic, didn't affect the outcome.
