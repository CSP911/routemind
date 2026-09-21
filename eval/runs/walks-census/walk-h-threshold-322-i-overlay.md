1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Dinner with a client, around 12 million won, locked in for three years: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount + multi-year term suggests a procurement/contract threshold question, not a one-off expense" --member /v1/regions/expense "dinner with a client sounds like entertainment expense reimbursement"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3fd65a --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m3/body

2. **Answer**
The division director signs it off. Yes — three competing quotes are needed first. (Delegation limit for this row: 20,058 thousand KRW; working days to expect: 10.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body — maps "dinner with a client" to category C4
/v1/nodes/hard-threshold-legend-amount/body — maps "around 12 million won" to amount V3
/v1/nodes/hard-threshold-legend-term/body — maps "locked in for three years" to term M3
/v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m3/body — the row itself (signer, quote count), in force from 2026-01-01

4. **Notes**
The question reads like an expense claim ("dinner with a client") but the three-year lock-in is the tell that this is actually a procurement/contract-threshold question, not a one-off entertainment expense — the expense region's tables (corp-card, evidence, travel-expense) don't have a concept of "term" at all. I opened both /v1/regions/procurement and /v1/regions/expense as overlay members to keep the choice visible, but only procurement's threshold table had anything answering "whose signature" or "how many quotes" for a multi-year commitment.

All three legend lookups (category, amount, term) happened to be exact matches to the phrasing in the question ("dinner with a client", "around 12 million won", "locked in for three years" all appear verbatim in the legend tables), so there was no need to round to a nearest band — worth flagging only because the legends explicitly warn you may have to take the nearest entry if your figure isn't listed, and I had to check that this case wasn't one of those.

The threshold table's own header states it is "in force from 2026-01-01" and supersedes two older versions (v2 and an original), with a legend-revision node explaining which dates each version covers. Today's date (2026-09-21) falls inside the current version's range, so I did not need to open the revision-legend or the superseded v2 table — but this is exactly the kind of place a stale answer could sneak in if the date weren't checked against it first.
