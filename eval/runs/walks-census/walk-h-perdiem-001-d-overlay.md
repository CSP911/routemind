1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G1, band B1, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per diem and receipt retention threshold are expense policy topics"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f518b0 --outcome answered --used /v1/nodes/sec-hard-perdiem/body /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body

2. **Answer**: Lodging cap is 99 USD per night. A receipt must be kept for any spend above 21 USD (the receipt threshold). This is from the current overseas per-diem table, in force from 2026-01-01, applicable since today (2026-09-21) falls after that date.

3. **Source**:
- /v1/nodes/sec-hard-perdiem (table, to locate the exact row)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body (the row read, containing the figures)

4. **Notes**: The overlay listing surfaced a warning up front — "overseas per-diem has THREE versions with different dates" (`hard-perdiem-legend-revision`) plus a superseded version `hard-perdiem-v2` (2024-07-01 to 2025-12-31). It would have been easy to grab the wrong version's figures without checking effective dates; I confirmed the row I read explicitly states "In force from 2026-01-01," which covers today's date (2026-09-21), so I didn't need to open the legend-revision or v2 documents at all — the exact G1/B1/S2 row existed directly in the current table's listing, so no legend lookups for grade/band/stay codes were needed either. Also worth flagging: when closing the overlay, I named `/v1/nodes/sec-hard-perdiem/body` as used, but I had only opened `/v1/nodes/sec-hard-perdiem` (the table listing, no `/body`) — the tool flagged both close addresses as "reached... from somewhere the overlay never named" rather than erroring, which suggests the address I supplied for the table listing wasn't quite the one it wanted credited. The actual figures came only from the row document, `hard-perdiem-row-grade-g1-band-b1-stay-s2/body`.
