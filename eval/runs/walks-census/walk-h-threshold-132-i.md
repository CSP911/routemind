1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body

2. **Answer**
The division director signs it off. Yes — three competing quotes plus a written comparison are required first. This is within the row's delegation limit (100,030 thousand KRW), so no excess-approval process applies.

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "about 40 million won" → amount V4)
- /v1/nodes/hard-threshold-legend-term/body (mapped "locked in for three years" → term M3)
- /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body (the answer: signer, quotes)

4. **Notes**
The table /v1/nodes/sec-hard-threshold listed 64 individual row files with no way to jump straight to the right one — had to read all three legend files first to translate the plain-English description into a category/amount/term code, then construct the row address from those codes (matching the naming pattern the table itself showed for other rows, not guessing blind). This is the current table (in force since 2026-01-01); the listing flagged two older, superseded versions (`hard-threshold-v2`, `threshold-table`) and a legend-revision warning file, which I deliberately avoided reading since today's date (2026-09-20) falls under the current table's validity window — reading those would have risked pulling stale figures. Worth flagging: "about 40 million won" sits almost exactly at this row's own delegation limit (100,030 thousand KRW is the ceiling for a much larger band, not this specific amount) — the limit shown belongs to the V4 band as a whole, not a 40M-specific ceiling, so I did not claim the request is "close to a limit."
