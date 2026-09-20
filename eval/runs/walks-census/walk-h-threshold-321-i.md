1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body

2. **Answer**: The department head signs it off, and yes — three competing quotes are required. (Category C4 "dinner with a client", amount V3 "around 12 million won", term M2 "renewing every year"; delegation limit for this row is 20,057 thousand KRW, so 12M falls within it; 9 working days to expect.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m2/body

4. **Notes**: The "dinner with a client, renewing every year" framing is misleading at first glance — it reads like an expense/entertainment question, and the expense region's table (with its "entertainment cap" blurb) looked like a plausible starting point. But the actual questions asked ("whose signature," "other prices first" i.e. quotes) are procurement-approval-threshold questions, not expense-cap questions, and the category legend confirms "dinner with a client" is explicitly mapped to C4 in the procurement threshold legend — so this belongs in procurement, not expense. Also worth flagging: the threshold table has three historical versions (a legend-revision warning, `hard-threshold-v2` superseded, and the current `sec-hard-threshold`); I only read the current one since it's stated in force from 2026-01-01 and today is 2026-09-21, but it would be easy to grab the superseded v2 row by mistake if not careful about dates.
