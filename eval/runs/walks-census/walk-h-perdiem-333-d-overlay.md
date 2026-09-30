1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G4, band B4, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade, band, stay - should have hotel nightly cap" --member /v1/nodes/evidence "what has to be attached for a spend to be accepted - receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_0f3129 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body

2. **Answer**
Lodging (hotel), per night: 347 USD. Receipt threshold: 66 USD (a receipt must be kept for any spend above this amount). This is the current table, in force from 2026-01-01.

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s4/body

4. **Notes**
The overlay members I picked (`/v1/nodes/sec-hard-perdiem` and `/v1/nodes/evidence`) were both tables/section-heads, not the leaf row itself — `sec-hard-perdiem`'s table expansion is what actually printed the per-grade/band/stay rows, one of which (`hard-perdiem-row-grade-g4-band-b4-stay-s4/body`) matched G4/B4/S4 exactly and answered both parts of the question in one row (lodging cap and receipt threshold are columns in the same table, not separate documents). I never needed the `/v1/nodes/evidence` member or its qualified-evidence table — the per-diem row already carries its own receipt threshold, so pulling the general evidence-qualification table would have been redundant here (though it could matter if the question were about what *kind* of document counts as a receipt, not the dollar threshold).

One genuine gotcha: the expense area table warned there are three versions of this per-diem table (`hard-perdiem-legend-revision`, `hard-perdiem-v2` superseded 2024-07-01 to 2025-12-31, and an older `overseas-rates`). I had to make sure I was reading the current one — `sec-hard-perdiem` is explicitly labeled "in force from 2026-01-01" and today is 2026-09-20/21, so it's the right version. Easy to grab the wrong version if you don't check the effective-date labels.

Also worth flagging: `overlay close` reported the used address as "reached" rather than a named member, i.e. it didn't consider the row address I read to be one of the addresses I'd explicitly added to the overlay (I'd added the parent table addresses, not the leaf row). Didn't affect the answer, but it means the overlay bookkeeping is stricter about exact-address matches than I expected.
