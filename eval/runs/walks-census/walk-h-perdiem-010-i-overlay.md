1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Junior analyst, Singapore, one night — hotel per-night cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table, likely has hotel caps by grade/destination band/stay length" --member /v1/nodes/evidence "evidence table likely states receipt threshold above which a receipt must be kept"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_bb1406 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body

2. **Answer**: Lodging cap is 111 USD per night. The receipt threshold is 27 USD — above that amount, a receipt must be kept. (This is from the current overseas per-diem table, in force since 2026-01-01: junior analyst = grade G1, Singapore = band B2, one night = stay S1.)

3. **Source**:
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s1/body

4. **Notes**: The overlay's member rows (all 64 grade×band×stay combinations under sec-hard-perdiem) turned out not to be individually addressable as overlay members — closing with the row addresses came back "reached" rather than "used," meaning the overlay only tracked the two table-level members I originally added, not the leaf files I actually read. Doesn't affect the answer, just worth flagging if the scoring cares about that distinction.

The near-miss: the question's second half ("above what amount do I have to keep the receipt") sounds like a general expense-evidence question, and the expense area table surfaces /v1/nodes/qualified-evidence as a plausible match — it literally advertises "the ceiling on a simple receipt." I checked it and it's a different, unrelated rule (a KRW-denominated domestic qualifying-evidence table with a 30,000 KRW simple-receipt ceiling and a 2% penalty clause) — nothing to do with overseas per-diem or Singapore. The per-diem row itself already carries a "Receipt threshold" field (27 USD) that directly answers the question in context, so I used that instead. Had I not checked qualified-evidence, I might have second-guessed which was correct; had I used it instead of the per-diem field, I'd have given a currency-mismatched, wrong answer.

Also worth noting: "Singapore" in the question reads as the destination, not the analyst's home base — the band legend confirms Singapore maps to a destination band (B2), which is what the per-diem table indexes on, so that reading was correct and there was no real ambiguity there.
