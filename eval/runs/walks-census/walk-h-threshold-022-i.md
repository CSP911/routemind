1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body

2. **Answer**: The division director signs it off. Yes — three competing quotes are required first. (Delegation limit for this row is 20,010 thousand KRW; expect 10 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m3/body

4. **Notes**: The procurement table flagged that the approval threshold has three historical versions (`hard-threshold-legend-revision` warns of this) — easy to grab a superseded row (`hard-threshold-v2`, in force 2024-07-01 to 2025-12-31, or the older `threshold-table`) by mistake. I confirmed `sec-hard-threshold` is the one in force from 2026-01-01, which covers today's date (2026-09-20), and used that. The three axes (category/amount/term) are each resolved through a separate legend file rather than being guessable from the question's wording — "a couple of laptops" → C1, "around 12 million won" → V3, "locked in for three years" → M3 — and the row address has to be hand-assembled from those three codes exactly as the legends name them (c1/v3/m3), which is the one place in this walk where a typo would silently point at a nonexistent or wrong row.
