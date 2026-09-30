1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "I have a claim dated in 2025 and I am not sure which version of the approval threshold applies to it. Where is that written down?" --member /v1/regions/procurement "approval threshold by category, amount and term - most direct match for 'approval threshold'" --member /v1/regions/expense "claim likely refers to expense claim; may reference approval threshold versioning" --member /v1/regions/approval "approval chain docs may reference threshold versions/effective dates"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_71a816 --address /v1/regions/expense --why "claim in this question refers to an internal spend/approval claim, not an expense-report claim; no expense doc addressed threshold versioning"
./bench/rmcli.py overlay close --id ov_2026-09-20_71a816 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-v2/body /v1/nodes/hard-moved-threshold/body

2. **Answer**:
Approval threshold has three written versions, and the date on the claim decides which applies:
- until 2024-07-01: the original table (`threshold-table`), indexed by one qualifier
- 2024-07-01 to 2025-12-31: the second version (`hard-threshold-v2`), indexed by category + amount
- 2026-01-01 onwards: the current table (`sec-hard-threshold`), which adds term as a third qualifier

A claim dated anywhere in 2025 falls in the middle band (2024-07-01 to 2025-12-31), so the applicable version is `hard-threshold-v2`, whose amount bands by category are:
| category | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| C1 | 1000k KRW | 5001k KRW | 20002k KRW | 100003k KRW |
| C2 | 1004k KRW | 5005k KRW | 20006k KRW | 100007k KRW |
| C3 | 1008k KRW | 5009k KRW | 20010k KRW | 100011k KRW |
| C4 | 1012k KRW | 5013k KRW | 20014k KRW | 100015k KRW |

None of the three versions carries a note saying it was superseded — the oldest in particular says nothing about being replaced — so date-checking against the legend page is mandatory rather than optional.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (which version covers which date range)
- /v1/nodes/hard-threshold-v2/body (the 2025-applicable version, with the actual figures)
- /v1/nodes/hard-moved-threshold/body (confirms this subject lives under procurement from 2026-01-01 onward, not approval — relevant only for dates on/after that cutover, not for this 2025 claim)

4. **Notes**:
The word "claim" pulled me toward /v1/regions/expense first, expecting an expense-claim reimbursement doc. That region had nothing about threshold versioning at all — the only per-diem versioning page there (`hard-perdiem-*`) is a different subject. The actual hit was under /v1/regions/procurement, where "approval threshold" is a named, versioned subject with its own legend page. I removed the expense member from the overlay once it was clear it contributed nothing.
A second trap: /v1/regions/approval also surfaced a very on-topic-looking file, `hard-moved-threshold/body`, which says thresholds moved to procurement "from 2026-01-01." Read carelessly, this could be mistaken for the answer itself, but it's about where the *current* (2026+) table lives, not about a 2025 date — for a 2025 claim it's background, not the source of the figures.
The legend page (`hard-threshold-legend-revision/body`) was the key artifact: it states outright that none of the three versions marks itself as superseded, and that reaching for the newest table is wrong for anything before 2026-01-01. Without it, the natural (wrong) move would have been to grab `sec-hard-threshold` (the current table) just because it's labeled "current" and appears first alphabetically-ish in the listing.
