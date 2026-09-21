1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G1, band B2, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of three versions of per-diem; need to confirm which applies to today's date"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_31c932 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s2/body

2. **Answer**:
Lodging cap: 115 USD per night. Receipt threshold: 30 USD (a receipt must be kept for spend above this amount).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-row-grade-g1-band-b2-stay-s2/body

4. **Notes**:
Overseas per-diem exists in three versions (`overseas-rates` until 2024-07-01, `hard-perdiem-v2` 2024-07-01 to 2025-12-31, `sec-hard-perdiem` from 2026-01-01), and the legend-revision page warns the oldest version never says it was superseded — checking today's date (2026-09-21) against that table before trusting any figure was the important step, not something to skip. Today falls in the current-table window, so `sec-hard-perdiem` / the G1-B2-S2 row under it is correct.

The only mildly confusing bit: creating the overlay against `/v1/nodes/sec-hard-perdiem` auto-expanded to list every grade/band/stay row in that table (68 rows), including the exact G1-B2-S2 row I needed — so no separate `table` call on `sec-hard-perdiem` was needed. When closing, the tool flagged the row address as "reached ... from somewhere the overlay never named," even though it had been printed in the overlay's own listing — a bookkeeping quirk, not a wrong address; the address itself was exactly as printed and needed no correction.
