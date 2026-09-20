1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py read /v1/nodes/threshold-table/body

2. Answer
Under the version in force on 2025-08 (the 2024-07-01 to 2025-12-31 version), category C2, amount band V2 has a delegation limit of 5,005 thousand KRW (5,005,000 KRW).
This document states that who signs, quote count, and turnaround "followed the approval thresholds rule unchanged" — i.e. the pre-2024-07-01 one-qualifier table. V2 is the second of four bands (V1-V4), which lines up positionally with the second of four rows in that unchanged rule: Division head, delegated, 2 quotes.

3. Source
/v1/nodes/hard-threshold-legend-revision/body (established which of the three versions applies to an August 2025 date)
/v1/nodes/hard-threshold-v2/body (the in-force version; gives the C2/V2 amount figure and states the signer rule was carried over unchanged)
/v1/nodes/threshold-table/body (the unchanged one-qualifier signer rule referenced by the v2 document)

4. Notes
The obvious trap here is reaching for the current table (sec-hard-threshold, in force from 2026-01-01) since it was the one listed as "current" in the procurement area table — the legend-revision page exists specifically to warn that a 2025 date needs the *middle* of three versions, not the newest.
The bigger snag: the v2 table is literally headed "Who signs it, by category and amount" but its cells contain only KRW figures, no signer names. Reading it too quickly could produce "not found" for the signer half of the question. The document's closing line clarifies that signer/quotes/turnaround were not redefined in this version and still follow the old, category-blind table — so the V1-V4 columns have to be read as standing in, positionally, for the four tiers of that old table (team lead / division head / CEO / CEO with proposal). That mapping is inferred from the text, not stated as an explicit crosswalk, so I flag it as the least certain part of the answer.
