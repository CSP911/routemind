1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body

2. **Answer**: For grade G2, band B3, stay S4: lodging cap is 203 USD per night. A receipt must be kept for any spend above 49 USD (the receipt threshold). This is from the current overseas per-diem table, in force since 2026-01-01, which applies as of today (2026-09-20).

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s4/body

4. **Notes**: The expense area's table listing flagged upfront that overseas per-diem has three versions in force at different times (`overseas-rates`, `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, and the current `sec-hard-perdiem` from 2026-01-01). It would have been easy to grab a superseded row by mistake — I deliberately picked `sec-hard-perdiem` since today's date (2026-09-20) falls in its range, and confirmed the row itself restates the same effective date. The row's grade/band/stay address was exact and unambiguous once inside the per-diem table, so no guessing was needed there. One thing to flag for whoever asked: the question conflates "what can I put on a hotel each night" with the per-diem lodging cap — those are the same number here, but the table also has a separate "if figures are exceeded" clause (excess not pre-approved is not recoverable at all; unavoidable excess needs a written statement and budget-holder sign-off), which the short question doesn't ask about but is likely relevant in practice.
