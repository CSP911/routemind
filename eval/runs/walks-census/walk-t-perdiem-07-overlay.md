1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "How many times has the overseas per-diem been rewritten, and from what date does each version apply?" --member /v1/regions/expense "per-diem / overseas travel allowance rates and history likely live in the expense region"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py overlay add --id ov_2026-09-20_f76a19 --address /v1/nodes/overseas-rates/body --why "the oldest of the three per-diem versions, in force until 2024-07-01, confirmed by the legend-revision doc and by hard-perdiem-v2's own text"
./bench/rmcli.py overlay close --id ov_2026-09-20_f76a19 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/overseas-rates/body /v1/nodes/hard-perdiem-v2/body /v1/nodes/sec-hard-perdiem

2. **Answer**:
The overseas per-diem has been written three times in total — i.e. rewritten twice since the original:
- Version 1 (original — "Overseas allowance and exchange rate"): in force until 2024-07-01. No start date is given for this version; it carries no note that it was ever superseded.
- Version 2 (first rewrite — "Overseas per-diem, second version"): in force from 2024-07-01 to 2025-12-31.
- Version 3 (second rewrite — the current table): in force from 2026-01-01 onwards.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (the index stating there are three versions and the date each covers)
- /v1/nodes/overseas-rates/body (version 1, the original)
- /v1/nodes/hard-perdiem-v2/body (version 2, 2024-07-01 to 2025-12-31)
- /v1/nodes/sec-hard-perdiem (version 3, current, from 2026-01-01)

4. **Notes**:
The overlay's initial member list (from /v1/regions/expense) surfaced the legend-revision doc and hard-perdiem-v2 directly, but not the oldest version's address — it only names it by the short label `overseas-rates` inside the doc text, not as a full address. I had to go back down through /v1/nodes/travel-expense → /v1/nodes/travel-overseas to find the actual address /v1/nodes/overseas-rates/body; it never appeared in the expense region's table at all, only nested under travel-overseas. That's the one place I nearly gave up and reported "not found" for the oldest version's precise identity.

The trickiest part is the count itself: the legend-revision doc says "this subject has been written three times," which is 3 versions total but only 2 rewrites of the original — the question asks how many times it's been "rewritten," which I read as excluding the initial writing. I called out both numbers above rather than picking one, since the doc's own phrasing invites the ambiguity.

Also worth flagging: the legend-revision doc explicitly warns that "the oldest says nothing at all about having been replaced," and reading overseas-rates/body confirms this — it has no reference to later versions. Anyone reading only that file would incorrectly assume it's still current. The only reason I know it isn't is because hard-perdiem-v2 and the legend-revision doc both mention it by name from the other direction.
