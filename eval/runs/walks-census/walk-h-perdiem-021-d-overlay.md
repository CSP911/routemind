1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G1, band B3, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per-night cap and receipt threshold are travel/expense policy figures"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_109ead --outcome answered --used /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body

2. **Answer**: Lodging cap is 131 USD per night. The receipt threshold is 39 USD — spend above that amount requires a receipt.

3. **Source**:
/v1/nodes/sec-hard-perdiem
/v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s2/body

4. **Notes**: The expense area table listed 20 candidate rows, but the exact match was obvious once opened — `sec-hard-perdiem` is explicitly labeled "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01," and it directly indexes by grade/band/stay codes, giving an exact row address for G1/B3/S2 with no interpretation needed. The one thing worth flagging: this table has two superseded predecessors (`hard-perdiem-v2` covering 2024-07-01 to 2025-12-31, and an older `overseas-rates`), called out via a `hard-perdiem-legend-revision` warning row. Since today's date (2026-09-21) falls within the current table's stated effective range and the row itself repeats "In force from 2026-01-01," I didn't need to open the legend-revision doc to disambiguate — but a walker who grabbed a row from `hard-perdiem-v2` by habit or an old bookmark would silently get a stale figure. Also worth noting: the overlay close reported both addresses as "reached" rather than matched members, since I navigated to them through the table rather than adding them as explicit overlay members — the answer is still correctly sourced, just via table traversal instead of member curation.
