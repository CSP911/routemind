1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body

2. **Answer**
Under the version of supplier due diligence in force in January 2024 (the original, single-qualifier version, in force until 2024-07-01), a new supplier had to pass three checks before registration:
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen — whether the entity or its owners had been flagged before

A sanctions hit or a refused code of conduct stopped registration outright, with no delegated sign-off able to override it.

3. **Source**
/v1/nodes/supplier-due-diligence/body (the oldest version, in force until 2024-07-01 — the one covering January 2024)
Also consulted for version selection: /v1/nodes/hard-diligence-legend-revision/body

4. **Notes**
The procurement table (/v1/regions/procurement) only lists the current (sec-hard-diligence, from 2026-01-01) and second (hard-diligence-v2, 2024-07-01 to 2025-12-31) versions of supplier due diligence directly — it does not list the oldest version's address at all, even though the legend-revision page (hard-diligence-legend-revision) explicitly warns that three versions exist and names the oldest one's address as `supplier-due-diligence`. Taking the procurement table's row list at face value would have led to wrongly answering from hard-diligence-v2 (which only covers 2024-07-01 onward, not January 2024) or missing the oldest version's existence entirely. The oldest version's address only turned up by going through the "where to start" overview table (/v1/nodes/sec-supplier-due-diligence), which happens to link to it as one of "four due-diligence pages." The legend page's warning that "the oldest says nothing at all about having been replaced" also matters: the document itself gives no internal clue it's superseded, so without checking the legend first I'd have had no way to know this page wasn't current.
