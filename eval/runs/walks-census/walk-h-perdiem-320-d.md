1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body

2. **Answer**: For grade G4, band B3, stay S1 (in force from 2026-01-01, which covers today's date 2026-09-20): the hotel/lodging cap is 319 USD per night. A receipt must be kept for any spend above 48 USD (the receipt threshold). (For context, not asked: meals are 93 USD/day, incidentals 19 USD/day.)

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to today's date)
/v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s1/body (the figures)

4. **Notes**: The expense area table flags up front that overseas per-diem has three superseded/current versions, and warns explicitly that "the oldest says nothing at all about having been replaced" and that reaching for the newest table is wrong for dates before 2026-01-01. That's the trap here — it would have been easy to jump straight to `sec-hard-perdiem` without checking, and gotten the right answer by luck since today (2026-09-20) does fall in the current version's range, but only after actually reading the revision legend was I sure this wasn't one of the 2025-dated questions that needs `hard-perdiem-v2` instead. Once inside `sec-hard-perdiem`, the row list is a flat 64-row grid indexed by grade × band × stay, but the exact row `hard-perdiem-row-grade-g4-band-b3-stay-s1` was already spelled out with the given codes, so no legend lookups for grade/band/stay definitions were needed — the question supplied the codes directly rather than descriptions to translate.
