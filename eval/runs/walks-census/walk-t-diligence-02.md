1. Commands:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body

2. Answer:
Under the version of supplier due diligence in force in September 2023 (the original version, in force until 2024-07-01, indexed by "one qualifier" — i.e. not split by origin/value/goods), a new supplier required three checks before registration:
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen — whether the entity or its owners had been flagged before
A sanctions hit or a refused code of conduct stopped registration outright, with no delegated sign-off able to override it.

3. Source:
- /v1/nodes/hard-diligence-legend-revision/body (used to determine which of the three versions applies to September 2023)
- /v1/nodes/supplier-due-diligence/body (the oldest version, in force until 2024-07-01, containing the actual answer)

4. Notes:
The procurement area table surfaces the CURRENT due-diligence table (sec-hard-diligence) and the SECOND version (hard-diligence-v2) prominently, both labeled with their date ranges, but the oldest/original version's address (supplier-due-diligence) is not listed directly in that table's rows — it only turned up one level deeper, under /v1/nodes/sec-supplier-due-diligence (the "where to start" overview table for the four due-diligence pages). Without first reading the legend-revision page, it would have been easy to assume the only two options were the v2 (2024-07-01 to 2025-12-31) or current (2026-01-01 onward) tables, since those are the ones with obvious "superseded"/"current" labels at the procurement level — and to wrongly apply hard-diligence-v2 to a 2023 date since it's the "older" of the two visible options. The legend explicitly warns that the oldest version "says nothing at all about having been replaced," which matches: the supplier-due-diligence/body document reads as a normal, current-sounding policy page with no version markers, so date-checking against the legend first was necessary to avoid misattributing it or missing it entirely.
