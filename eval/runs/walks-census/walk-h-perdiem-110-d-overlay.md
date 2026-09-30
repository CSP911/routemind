1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G2, band B2, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel cap and receipt threshold" --member /v1/nodes/hard-perdiem-legend-revision "warns about three versions of per-diem, need to confirm which is current for 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_023df8 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**: Lodging cap is 175 USD per night. The receipt threshold is 31 USD — above that amount, evidence (a receipt) has to be kept/attached.

3. **Source**:
- /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s1/body (the figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms this 2026-01-01-onwards table is the one in force for today's date, 2026-09-20)

4. **Notes**: The expense area table flags up front that overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), so the real risk here was landing on a stale table by grabbing the first per-diem-looking row instead of the one indexed by all three qualifiers (grade/band/stay). I deliberately opened the revision-legend page before trusting the figures, since it says explicitly that reaching for the newest is only right for questions dated 2026-01-01 or later — today's date (2026-09-20) clears that bar, so `sec-hard-perdiem` was correct, but it would have been wrong for a question dated in 2025. Once inside the current table, the target row (grade-g2-band-b2-stay-s1) was named exactly by the working set with no ambiguity — no grade/band/stay legend lookups were needed since the question stated all three qualifiers directly.
