1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py table /v1/nodes/supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/sec-hard-diligence/body

2. Answer

35 (the value at the intersection of origin O2 and value band W2 in the March-2025-in-force table).

That table only varies the "checks required" figure by origin × value; per the same page, the documents to collect and the re-review interval were not varied by origin/value in this version and followed the original (pre-2024-07-01) supplier due diligence rule unchanged — i.e. the same three-part screen described on that oldest page (sanctions/ownership check against restricted-party lists, signed code-of-conduct acknowledgement, and a basic disqualification screen), with the O2/W2 cell contributing the figure 35 on top of that. No legend anywhere in the procurement region decodes what "35" itself stands for beyond being the table's own figure for that cell — I could not find a page that translates it into a named check or procedure.

3. Source

/v1/nodes/hard-diligence-legend-revision/body (established March 2025 falls under the second/v2 version)
/v1/nodes/hard-diligence-v2/body (the O2×W2 table cell = 35, and the note on unchanged documents/re-review interval)
/v1/nodes/supplier-due-diligence/body (the unchanged three-check content referenced by the note above)

4. Notes

The three-version legend page (hard-diligence-legend-revision) was essential and easy to get right here — it explicitly flags 2025 dates as the case "where taking either extreme is wrong," so I didn't default to the current (sec-hard-diligence) table just because it was listed first and most prominently in the procurement region ("THE CURRENT SUPPLIER DUE DILIGENCE TABLE").

The genuinely confusing part was the v2 table itself. Its header reads "The checks required, by origin and value" over a table of bare numbers (30–45), which reads like a screening-level code that should be decoded by a legend — the current (2026) table's row pages use exactly that pattern (hard-diligence-row-origin-o2-value-w2-goods-k1/body etc., each with real prose describing checks/documents/interval). I went looking for an equivalent legend or row-page for the v2 numbers and confirmed via the procurement region listing that none exists — v2 is a flat, single-page table with no sub-legend. I nearly reported "not found" on the grounds that the number is uninterpretable, but the footnote on the v2 page ("the checks required, the documents to collect and the re-review interval beyond the column above followed the supplier due diligence rule unchanged until 2026-01-01") indicates the qualitative screen (the three checks) is the unchanged baseline from the oldest page, and the table's number is the one thing that does vary by origin/value — so I'm reporting both: 35 as the literal figure, and the unchanged three-check content as the substance behind it. I'd flag this cell as the most likely place a reader gets the wrong figure by misreading rows/columns (origin down the left, value across the top) or by pulling from the current three-qualifier table instead of the March-2025 two-qualifier one.
