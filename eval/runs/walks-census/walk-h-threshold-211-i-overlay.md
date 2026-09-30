1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, roughly 3 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount+term based approval threshold, and whether competitive quotes are required, likely covers this" --member /v1/regions/approval "whom to put in the approval chain / whether a team lead can sign off"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e08a14 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body

2. **Answer**
The department head signs it off, and two competing quotes are required. This is category C3 (flights and hotels), amount V2 (roughly 3 million won — delegation limit 5,037 thousand KRW for this row), term M2 (renewing every year). Expect 6 working days. This is the current threshold table, in force from 2026-01-01, so it applies as of today (2026-09-21).

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body

4. **Notes**
Nothing here was actually ambiguous once the three legends were read — the whole trick of this table is that the question's plain-language description ("flights and hotels", "roughly 3 million won", "renewing every year") has to be translated through the category/amount/term legends before the row address can even be built, and each legend is a separate document. I nearly reached for the /v1/regions/approval area first since "whose signature" sounds like an approval-chain question, but that region's own hard-moved-threshold note says spend approval thresholds moved to procurement on 2026-01-01 — so approval's tables would have been the wrong (superseded) source for this. I did not check the older hard-threshold-v2/threshold-table versions since sec-hard-threshold is explicitly the current table (2026-01-01 onward) and today's date falls inside that range.
