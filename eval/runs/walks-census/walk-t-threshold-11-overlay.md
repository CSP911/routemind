1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Delegation limit / signer for a purchase of 2,000,000 KRW net of VAT in 2023, and what it became by 2025" --member /v1/regions/procurement "approval threshold by category, amount, term - current table plus likely history"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay add --id ov_2026-09-20_1944f4 --address /v1/nodes/threshold-table --why "oldest version, in force until 2024-07-01, covers 2023"
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay remove --id ov_2026-09-20_1944f4 --address /v1/nodes/threshold-table --why "not a real printed address - was guessed from legend's 'where' column text, not an address from a table"
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py overlay add --id ov_2026-09-20_1944f4 --address /v1/nodes/threshold-table/body --why "actual oldest threshold table address, found via purchase-request > approval-threshold"
./bench/rmcli.py overlay add --id ov_2026-09-20_1944f4 --address /v1/nodes/approval-threshold --why "parent table leading to the oldest threshold-table/body"
./bench/rmcli.py read /v1/nodes/threshold-table/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py table /v1/nodes/sec-bands-and-quotes-in-practice
./bench/rmcli.py read /v1/nodes/band-reference-table/body
./bench/rmcli.py table /v1/nodes/hard-threshold-v2
./bench/rmcli.py overlay close --id ov_2026-09-20_1944f4 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/threshold-table/body /v1/nodes/hard-threshold-v2/body

2. **Answer**
2023: 2,000,000 KRW net of VAT falls in the 500,000–3,000,000 KRW band → **Division head, delegated** (2 quotes required).

2025: the flat 500,000/3,000,000/10,000,000 bands were replaced by category-specific cutoffs (categories C1–C4, each with its own V1–V4 amount boundaries, e.g. C1: V1=1,000,000 / V2=5,001,000 / V3=20,002,000 / V4=100,003,000 KRW; the other categories' boundaries differ only slightly). 2,000,000 KRW falls between V1 (~1,000,000–1,012,000, depending on category) and V2 (~5,001,000–5,013,000) for every one of the four categories, so it lands in the same ordinal band (the second one) no matter which category the purchase is in. The document states that who signs, how many quotes, and how long it takes "followed the approval thresholds rule unchanged" from the old table — i.e. the same ordinal-band → approver mapping carries over. So the signer is still **Division head, delegated** (2 quotes) — unchanged in title from 2023, even though the amount cutoff defining that band moved from 500,000–3,000,000 up to roughly 1,000,000–5,000,000 (category-dependent).

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (establishes which of the three versions covers which date range)
- /v1/nodes/threshold-table/body (2023 answer)
- /v1/nodes/hard-threshold-v2/body (2025 answer)

4. **Notes**
- The trap here was building an address by hand. The legend page's "where" column literally printed `threshold-table` as a bare name (not a path), and it was tempting to prepend `/v1/nodes/` and use it directly — I did exactly that, and the overlay tool flagged it as "(nothing here)" rather than erroring, which was the tell that I'd fabricated an address instead of following a printed one. The real address, `/v1/nodes/threshold-table/body`, only turned up two hops later via `purchase-request` → `approval-threshold` → `threshold-table/body`. The `/v1/regions/procurement` table itself never lists the oldest version at all — only the v2 and current tables appear there, which made it look at first like the 2023 version wasn't in scope for this area.
- The 2025 figure required real computation, not a lookup: the v2 table doesn't name an approver directly, it only gives per-category amount cutoffs (V1–V4) and says the old approver/quote rule applies "unchanged." I had to check that 2,000,000 KRW lands in the same ordinal band (between V1 and V2) for all four categories before I could say the answer doesn't depend on which category the purchase is in — if the categories' V1/V2 values had straddled 2,000,000 differently, the question would have been unanswerable without knowing the category, and the question as asked doesn't supply one.
- I nearly used `/v1/nodes/band-reference-table/body` (reached via `sec-bands-and-quotes-in-practice`) as corroboration for the 2025 figure — it has the same clean 500,000/3,000,000/10,000,000 bands and looked current at a glance. But it sits as a sibling of `threshold-table/body` under the same `approval-threshold` parent, not under `hard-threshold-v2`, and its own text still cites "10,000,000 KRW and over" — the old cutoff. It's companion material for the *oldest* version only, and using it for 2025 would have silently given the wrong (superseded) band boundaries while landing on the same approver name by coincidence.
