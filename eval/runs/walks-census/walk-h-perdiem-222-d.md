1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body
./bench/rmcli.py table /v1/nodes/evidence

2. **Answer**:
Lodging (hotel), per night: 263 USD.
Receipt threshold: 50 USD — you must keep the receipt for spends above this amount.
(For reference, the same row also gives meals per day: 94 USD, and incidentals per day: 19 USD.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s3/body

4. **Notes**:
The expense region table flags up front that overseas per-diem has THREE versions in force at different times (`sec-hard-perdiem` current since 2026-01-01, `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, and `overseas-rates` before that) — easy to grab a superseded table if you don't check the date. Today is 2026-09-20, which falls under the current `sec-hard-perdiem` table, so that was the right pick, but it's the kind of thing that would silently give a wrong answer if skipped.
The per-diem table is a flat 64-row index (4 grades × 4 bands × 4 stays), so the grade/band/stay codes from the question map directly to one row address — no legend lookup was needed since the question already used the G3/B3/S3 codes verbatim.
I opened the `evidence` table to check whether "receipt threshold" in the per-diem row meant something narrower or different from the general receipt-evidence rules, but the per-diem row already states its own "Receipt threshold" figure explicitly (50 USD), so that was the answer and the evidence table wasn't actually needed — a bit of double-checking that turned out to be unnecessary but was cheap.
