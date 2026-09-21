1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G2, band B1, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01, matches the question's exact terms"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8efef2 --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body

2. **Answer**:
Lodging cap: 163 USD per night. Receipt required above: 25 USD.

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body

4. **Notes**:
The expense area table's own description warns overseas per-diem has THREE versions with different figures (hard-perdiem-v2 for 2024-07-01 to 2025-12-31, an older `overseas-rates`, and the current `sec-hard-perdiem` table in force from 2026-01-01). Today's date (2026-09-21) falls under the current table, so `sec-hard-perdiem` was the right pick, but it would be easy to grab the superseded `hard-perdiem-v2` node by mistake since it's listed right next to the current one in the area table with similar wording. Opening the `sec-hard-perdiem` table (rather than reading it directly, since it's a table-kind address) surfaced one row per grade/band/stay combination — the G2/B1/S2 address was printed exactly, so no address construction was needed. The row itself confirms its own effective date range in a footnote, which was useful for double-checking against today's date without a separate lookup.
