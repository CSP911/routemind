1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "How many times has the approval threshold been rewritten, and from what date does each version apply?" --member /v1/regions/procurement "approval threshold by category/amount/term lives here" --member /v1/regions/approval "approval chain rules might reference threshold history"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py overlay close --id ov_2026-09-20_feaee4 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-v2/body /v1/nodes/hard-moved-threshold/body

2. **Answer**:
The approval threshold has been rewritten twice — three versions exist in total, none formally withdrawn:
- Version 1 (original): in force until 2024-07-01. Held at `threshold-table`, indexed by one qualifier (no category or term breakdown).
- Version 2: in force from 2024-07-01 to 2025-12-31. Held at `hard-threshold-v2`, indexed by two qualifiers (category + amount).
- Version 3 (current): in force from 2026-01-01 onwards. Held at `sec-hard-threshold`, indexed by three qualifiers (category + amount + term). This version also moved organizationally from the approval region to the procurement region as of the same date (2026-01-01), per `hard-moved-threshold`.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (primary: states all three versions and their date ranges explicitly)
- /v1/nodes/hard-threshold-v2/body (confirms version 2's date range and cross-references the other two)
- /v1/nodes/sec-hard-threshold (confirms current version's start date, 2026-01-01)
- /v1/nodes/hard-moved-threshold/body (confirms the 2026-01-01 change was also an organizational move, not a fourth content rewrite)

4. **Notes**:
The region table's one-line description for procurement ("the approval threshold by category, amount and term — current tabl...") only hints at the current table, so it would be easy to stop at `sec-hard-threshold` and report just one version, missing that this subject has history at all. The overlay's row list surfaced a `hard-threshold-legend-revision` file with an explicit "THREE versions" warning, which was the load-bearing document — it directly states the count and the date boundaries, and warns that "the oldest says nothing at all about having been replaced," meaning nothing in the older documents themselves would tip you off to check for newer ones without this legend page.

A second trap: `/v1/nodes/hard-moved-threshold/body`, found under the approval region, describes thresholds being "moved to procurement" on 2026-01-01. This reads like it could be a fourth version or a separate rewrite event, but it's an organizational relocation of where the rule lives (approval region → procurement region), not a content rewrite — the content change on that date is the same one already counted as version 3. I read it to make sure I wasn't missing a rewrite, then excluded it from the count.

The oldest version's own address (`threshold-table`) was never printed by any table or overlay listing in this walk — it's only referenced by name inside other documents' text. I did not fetch it directly since I never received a printed address for it, per the "use addresses exactly as printed, never construct one" rule; the legend-revision page's own summary of it (no category/term breakdown, in force until 2024-07-01) was sufficient to answer the question.
