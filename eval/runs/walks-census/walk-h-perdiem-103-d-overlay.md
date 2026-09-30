1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G2, band B1, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01 — should hold the hotel cap" --member /v1/nodes/evidence "evidence table likely holds the receipt-required threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py overlay remove --id ov_2026-09-21_b9a3be --address /v1/nodes/qualified-evidence --why "general evidence-qualification table; the per-diem row itself already gives its own Receipt threshold figure specific to G2/B1/S4"
./bench/rmcli.py overlay remove --id ov_2026-09-21_b9a3be --address /v1/nodes/evidence --why "the per-diem row itself already carries its own Receipt threshold figure specific to G2/B1/S4; the general evidence table wasn't needed"
./bench/rmcli.py overlay close --id ov_2026-09-21_b9a3be --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body

2. **Answer**:
Lodging, per night: 171 USD. Receipt required above 31 USD. (This row also carries Meals, per day: 62 USD and Incidentals, per day: 12 USD, in force from 2026-01-01 — the current version.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s4/body

4. **Notes**:
The row's own "Receipt threshold" field is exactly the "above what amount do I have to keep the receipt" the question asks — it answered both halves of the question by itself, so opening the general evidence-qualification table (/v1/nodes/qualified-evidence) turned out unnecessary; I opened it anyway to check for a conflicting general rule before closing, found none relevant to per-diem specifically, and removed it from the overlay. The expense area table flagged that overseas per-diem has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem` from 2026-01-01); today's date (2026-09-21) falls inside the current version's range, and the row itself restates "In force from 2026-01-01," so no date-based ambiguity there. The one thing that could trip someone up: the exact grade/band/stay row address had to be assembled from the grade-g2-band-b1-stay-s4 pattern visible in the overlay listing rather than guessed — I only used addresses the tool printed, not a constructed one.
