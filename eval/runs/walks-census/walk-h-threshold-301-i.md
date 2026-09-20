1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body

2. Answer
The team lead signs it off. No competing quotes are required (0 needed at this band). Delegation limit for this row is 1,049 thousand KRW, and 700,000 won falls within it. Expect 3 working days.

3. Source
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m2/body

4. Notes
I first opened the expense area table because "dinner with a client" and "entertainment cap" pointed there, but that area only covers what the card may be used for and caps — not who signs or how many quotes. The actual answer lives under procurement's approval-threshold table, which is indexed by three orthogonal codes (category/amount/term) resolved through three separate legend files rather than free text — easy to miss that "dinner with a client" is itself a literal row in the category legend (mapped to C4) rather than something to classify by judgment. "Renewing every year" was also a literal legend entry (term M2), not an obvious cue — I almost read it as irrelevant flavor text about the dinner being a yearly tradition rather than a commitment-term qualifier. Confirmed the row's "in force from 2026-01-01" matches today's date (2026-09-20/21) so no superseded-version trap applied here.
