1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A consultant's time, around 12 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount+term threshold and approval signature, and whether competitive quotes/bids required"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_4223b8 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body

2. **Answer**
The department head signs it off. Yes — three competing quotes are required. This falls under category C2 (a consultant's time), amount band V3 (around 12 million won, delegation limit 20,025 thousand KRW), term M2 (renewing every year). Expect 9 working days. If the figure is exceeded without prior approval, the excess is not recoverable; an unavoidable excess needs a short written statement plus evidence, decided by the budget holder.

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "around 12 million won" → amount V3)
- /v1/nodes/hard-threshold-legend-term/body (mapped "renewing every year" → term M2)
- /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body (the actual row: signer, quotes, delegation limit)

4. **Notes**
The procurement region's working set surfaced a loud warning row (`hard-threshold-legend-revision`) about three historical versions of the threshold table, plus a superseded `hard-threshold-v2` sitting right next to the current `sec-hard-threshold`. It would be easy to grab the wrong vintage. I stuck with `sec-hard-threshold`, whose table header states it up front ("in force from 2026-01-01"), and today is 2026-09-21, so it's current — I didn't need to open the revision-legend or the superseded v2 body at all, since the current table's own header already settled the date question.

The three legends (category/amount/term) are mandatory reading, not optional context: the row addresses are built from codes (C2/V3/M2) that only the legends define, and the phrasing in the question ("a consultant's time", "around 12 million won", "renewing every year") maps one-to-one onto legend rows almost verbatim — but only if you check all three; skipping the term legend, for instance, could lead to grabbing a term-M1 (one-off) or term-M4 (until cancelled) row by guesswork instead of the correct M2 (annual renewal).

One process wrinkle: `overlay close --used` reported all four addresses as "reached ... answered from somewhere the overlay never named" rather than matched members. That's because I only added the top-level `/v1/regions/procurement` as an overlay member at creation and never ran `overlay add` for the individual legend/row files as I drilled down through the table hierarchy — I treated the overlay as a starting bookmark rather than continuously updating it. The answer itself is unaffected, but a stricter reading of the walk instructions would have had me `add` each file to the working set with a reason as I narrowed to it, rather than just reading through table calls.
