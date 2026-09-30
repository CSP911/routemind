1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py read /v1/nodes/overseas-rates/body

2. Answer
The overseas per-diem has been written three times (i.e. rewritten twice), with three versions:
- Version 1, "Overseas allowance and exchange rate" (region-band only, no grade/stay): in force until 2024-07-01. No start date is given anywhere found, and this document itself makes no mention of being superseded.
- Version 2, "Overseas per-diem, second version" (grade + band): in force 2024-07-01 to 2025-12-31.
- Version 3, "Overseas per-diem, current" (grade + band + stay): in force from 2026-01-01 onwards — this is the current table as of today (2026-09-22).

3. Source
/v1/nodes/hard-perdiem-legend-revision/body (revision table giving all three date ranges and the count "written three times")
/v1/nodes/hard-perdiem-v2/body (confirms version 2's own date range and cross-references the other two)
/v1/nodes/overseas-rates/body (the oldest version's own document, reached via /v1/nodes/travel-expense → /v1/nodes/travel-overseas)
/v1/nodes/sec-hard-perdiem (table description confirms version 3's 2026-01-01 start date)

4. Notes
- The expense area table advertises the legend page (/v1/nodes/hard-perdiem-legend-revision/body) right next to the current table (sec-hard-perdiem), which is exactly what saves this walk: it states up front that there are three versions and warns explicitly that grabbing the newest table is wrong for anything before 2026-01-01. Without that warning, the natural instinct given "the current table" language in the expense table's own row description would be to read only sec-hard-perdiem and miss two whole earlier versions.
- The legend page names the oldest version's location only as the bare word `overseas-rates`, not a full address — same in hard-perdiem-v2's prose ("the rule was the one in `overseas-rates`"). Neither is a proper printed address, so per the rules I could not just prepend /v1/nodes/ and read it. Had to reach it legitimately via /v1/regions/expense → /v1/nodes/travel-expense → /v1/nodes/travel-overseas, where it's listed as a genuine `file` row with address /v1/nodes/overseas-rates/body.
- The oldest version's own document (overseas-rates/body) never states when it took effect, and — as the legend page itself warns — never mentions being superseded at all. Its start date is genuinely not found anywhere in the documents I could reach; only its end date (until 2024-07-01) is known, and only from the legend page.
- Worth flagging: "how many times rewritten" is ambiguous between "3 versions exist" and "rewritten 2 times" (since the first version isn't itself a rewrite). I reported both framings to avoid the ambiguity silently picking one.
