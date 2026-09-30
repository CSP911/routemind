1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G2, band B2, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel nightly cap" --member /v1/nodes/evidence "evidence/receipt rules, likely has receipt threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ef114f --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body

2. **Answer**: Lodging cap is 187 USD per night. A receipt must be kept for any spend above 40 USD (the receipt threshold for this row).

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s4/body

4. **Notes**: The expense region table warns overseas per-diem has three versions (current since 2026-01-01, a superseded 2024-07-01–2025-12-31 version `hard-perdiem-v2`, and an older `overseas-rates`). I added `/v1/nodes/sec-hard-perdiem` to the working set specifically because its table description flags it as "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01," and today's date (2026-09-21) falls within that range, so I went straight for the row table rather than risk reading the superseded `hard-perdiem-v2` body. The overlay's rows go directly to per-grade/band/stay files, so opening it immediately surfaced the exact row needed (G2/B2/S4) without a further `table` call. The row itself already carries a "Receipt threshold" field (40 USD) alongside the lodging cap, so the separate `/v1/nodes/evidence` member I'd added (for a possibly-different general receipt-evidence threshold) turned out unnecessary — the per-diem row is self-contained and answers both parts of the question. I removed nothing but simply didn't need to visit `evidence`; closed citing only the row actually used.
