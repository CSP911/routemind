1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence

2. Answer
35 — the screening code required for an origin O2 supplier at contract value W2, under the supplier due diligence version in force 2024-07-01 to 2025-12-31 (which covers August 2025).

3. Source
/v1/nodes/hard-diligence-legend-revision/body (established which of the three versions applies to a 2025 date)
/v1/nodes/hard-diligence-v2/body (the O2 row × W2 column cell = 35)

4. Notes
The procurement table lists three separate supplier-due-diligence pages side by side — the oldest (`supplier-due-diligence`, pre-2024-07-01), the middle (`hard-diligence-v2`, 2024-07-01 to 2025-12-31), and the current (`sec-hard-diligence`, from 2026-01-01) — with no date filtering in the listing itself. It would be easy to grab the current table by reflex, since it's the one prominently marked "THE CURRENT ... TABLE" and has by far the richest content (64 individual row pages with full check descriptions, vs. the v2 table's bare numeric matrix). That would have been wrong: August 2025 falls in the middle version's window, and the legend-revision page explicitly warns this is "the case worth being careful about: it is the one where taking either extreme is wrong" (i.e., neither oldest nor current).

The v2 table only gives a bare number (35) at the O2/W2 intersection, with no per-cell narrative page like the current table's row pages provide. Its own text says the checks/documents/re-review interval "followed the supplier due diligence rule unchanged" beyond that column, but doesn't decode what the number 35 itself represents (no legend was found linking 30-45 to named checks). I checked the oldest `supplier-due-diligence` page and the `sec-supplier-due-diligence` overview looking for such a legend and found none — the oldest version predates origin/value qualifiers entirely (it names only three checks with no numeric coding), so it can't be used to decode v2's numbers either. I'm reporting the table value (35) as the answer since that is what the in-force document actually states, but flagging that no further decode of that code into a named screening procedure was found anywhere reachable from this table.
