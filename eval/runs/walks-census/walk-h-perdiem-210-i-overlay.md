1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Department head, Singapore, one night — hotel cap per night and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table (2026-01-01+), by grade/band/stay — should have hotel cap" --member /v1/nodes/evidence "evidence/receipt table — threshold above which a receipt must be kept" --member /v1/nodes/hard-perdiem-legend-revision "warns of 3 per-diem versions; need to confirm which is current for 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ed9487 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body

2. **Answer**: Hotel (lodging) cap is 239 USD per night. A receipt must be kept for any spend over 35 USD (the receipt threshold on this same row).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirms current table applies for 2026-09-20 dates)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Singapore → band B2)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body (lodging 239 USD/night, receipt threshold 35 USD)

4. **Notes**: The expense table warns up front that overseas per-diem has three versions indexed by date, and the revision-legend document is explicit that reaching for the newest version is wrong for dates before 2026-01-01 — today (2026-09-20/21) falls under the current table (`sec-hard-perdiem`), so no trap there, but it's the kind of thing that's easy to get wrong on an older-dated question. The three qualifiers (grade, band, stay length) are each resolved by a separate legend document rather than being guessable from the question text — "department head" isn't self-evidently G3, and Singapore isn't self-evidently B2, so skipping the legends would have been a guess, not an answer. I almost stopped after finding "Receipt threshold: 35 USD" directly on the per-diem row, but double-checked against /v1/nodes/qualified-evidence's general evidence table since the question's wording ("above what amount do I have to keep the receipt") sounded like it could be asking about the general evidence-qualification rule rather than the per-diem-specific one. That general table turned out to be denominated in KRW (30,000 KRW threshold) and about what class of document qualifies as evidence, not about per-diem hotel spend — using it here would have been the wrong number in the wrong currency for an overseas per-diem context. The per-diem row's own USD receipt threshold is the one that actually answers this question.
