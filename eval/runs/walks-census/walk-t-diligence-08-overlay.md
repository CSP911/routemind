1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Claim dated 2025: which version of supplier due diligence applies?" --member /v1/regions/procurement "supplier due diligence is a procurement topic"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_c60b3c --address /v1/nodes/contract-custody --why "not relevant, custody not diligence"  (failed — see Notes)
./bench/rmcli.py overlay add --id ov_2026-09-20_c60b3c --address /v1/nodes/hard-diligence-legend-revision/body --why "explains which of the three diligence versions covers 2025 dates"
./bench/rmcli.py overlay add --id ov_2026-09-20_c60b3c --address /v1/nodes/hard-diligence-v2/body --why "the actual 2024-07-01 to 2025-12-31 version applicable to a 2025-dated claim"
./bench/rmcli.py overlay remove --id ov_2026-09-20_c60b3c --address /v1/regions/procurement --why "narrowed to the two specific pages that answer the question"
./bench/rmcli.py overlay close --id ov_2026-09-20_c60b3c --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-v2/body

2. **Answer**
Supplier due diligence has been written three times, and which one applies is decided by the date on the claim, not by defaulting to the current table:
- until 2024-07-01: `supplier-due-diligence` (one qualifier)
- 2024-07-01 to 2025-12-31: `hard-diligence-v2` (two qualifiers — origin and value)
- 2026-01-01 onwards: `sec-hard-diligence` (three qualifiers — origin, value, and goods)

For a claim dated in 2025, the applicable version is the middle one, `hard-diligence-v2`: in force 2024-07-01 to 2025-12-31, indexed by origin (O1–O4) and value (W1–W4), giving the check-count matrix (e.g. O1/W1 = 30 checks through O4/W4 = 45 checks). Everything else about the process (documents to collect, re-review interval) followed the original, unversioned rule unchanged until 2026-01-01. This is explicitly called out as the case where reaching for either extreme (oldest or current) is wrong.

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (states the three versions and their date ranges, and that a 2025 date maps to the middle one)
- /v1/nodes/hard-diligence-v2/body (the actual middle-version content: date range and the origin/value check-count table)

4. **Notes**
- Overlay `remove` does not accept the browse-listing rows shown under a table-region member (e.g. `/v1/nodes/contract-custody`, which appeared when `/v1/regions/procurement` was added as a member) — those are just contents shown for browsing, not overlay members themselves. Trying to remove one by that address returns a 404 "not in this overlay." The fix was to `add` the specific file addresses I actually wanted as their own members, then `remove` the original `/v1/regions/procurement` member to narrow the working set down to just the two relevant files.
- The near-miss to watch for: the procurement table also holds a *current* supplier due diligence table (`sec-hard-diligence`) and a due-diligence "where to start" overview (`sec-supplier-due-diligence`). Grabbing either of those without checking `hard-diligence-legend-revision` first would have given a plausible-looking but wrong answer, since the current table only applies from 2026-01-01 and this claim is dated in 2025. The legend-revision page exists specifically to head off that mistake, and it says outright that the oldest version "says nothing at all about having been replaced" — so absence of a superseded notice on a page is not proof it's current.
