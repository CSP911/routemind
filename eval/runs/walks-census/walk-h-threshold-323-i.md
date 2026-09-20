1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m4/body

2. Answer
The division director signs it off, and yes — three competing quotes are needed first.
(Delegation limit for this row: 20,059 thousand KRW; expect about 11 working days.)

3. Source
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m4/body

4. Notes
The question mixes three separate qualifiers that only resolve through legend tables, not
by inspection: "dinner with a client" maps to category C4, "around 12 million won" maps to
amount V3, and "until we cancel it" (an open-ended, non-renewing commitment) maps to term
M4 — easy to misread as "renewing every year" (M2) if you don't notice the legend
distinguishes an indefinite/cancel-anytime arrangement from a fixed annual renewal.
The bigger trap was the date: the procurement area's approval-threshold subject has three
superseded versions (pre-2024-07-01, 2024-07-01–2025-12-31, and the current one from
2026-01-01), and the legend-revision page explicitly warns that reaching for the newest
table is wrong for anything before 2026-01-01, and that the oldest version says nothing
about having been replaced. Today's date (2026-09-20/21) put this squarely in the current
table, but I only knew that because I checked the revision legend before reading any row —
skipping that step would have risked silently using the wrong version without any warning
in the row itself.
