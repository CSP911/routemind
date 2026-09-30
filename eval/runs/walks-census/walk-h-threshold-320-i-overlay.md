1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Dinner with a client, around 12 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/expense "client dinner is an entertainment/business expense, need approval signer and rules" --member /v1/regions/procurement "12M won threshold may require competitive quotes before purchase"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_69f525 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body

2. **Answer**
The department head signs it off, and yes — three competing quotes are required before the spend. (Delegation limit for this row is 20,056 thousand KRW, so 12M won stays within the department head's authority; expect 8 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body

4. **Notes**
The top-level region list made this look like an expense/entertainment question first, so my initial overlay leaned on /v1/regions/expense. The actual answer lives entirely under /v1/regions/procurement's approval-threshold table, which turned out to already have "dinner with a client" as its literal example for category C4 in the category legend — a lucky, unambiguous match. The three legends (category, amount, term) each had to be read separately to translate the plain-language question ("dinner with a client" / "around 12 million won" / "just the once") into the C4/V3/M1 row address; nothing about the row address itself is guessable, so skipping any one legend would have made it impossible to find the right row among the 64 listed. I also checked that /v1/nodes/sec-hard-threshold is explicitly the version in force from 2026-01-01, matching today's date (2026-09-21), so I didn't need to consult the superseded v2/threshold-table versions — the legend-revision warning entries in the table were the tip-off that there were older versions to rule out.
