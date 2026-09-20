1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py read /v1/nodes/threshold-table/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold

2. Answer
2023: 2,000,000 KRW net of VAT falls in the 500,000–3,000,000 KRW band → **Division head, delegated** (2 quotes required).
2025: Same role, **Division head, delegated** (2 quotes). From 2024-07-01 to 2025-12-31 the amount column became category-specific (C1–C4), with "who signs," quote counts, and timing explicitly stated to have "followed the approval thresholds rule unchanged." The category boundaries for band 2 (V1–V2) are: C1 1,000,000–5,001,000 / C2 1,004,000–5,005,000 / C3 1,008,000–5,009,000 / C4 1,012,000–5,013,000 (all in KRW). 2,000,000 KRW falls inside the V1–V2 band for every one of the four categories, so regardless of which spend category applies, the sign-off is still Division head (delegated) — the amount range for that role just widened from 500,000–3,000,000 to roughly 1,000,000–5,013,000 KRW.

3. Source
/v1/nodes/hard-threshold-legend-revision/body (routing: which version covers 2023 vs 2025)
/v1/nodes/threshold-table/body (2023 answer)
/v1/nodes/hard-threshold-v2/body (2025 answer)

4. Notes
The legend-revision page was essential — there are three versions of this table (pre-2024-07-01, 2024-07-01→2025-12-31, and current from 2026-01-01), and it warns that the oldest "says nothing at all about having been replaced," so grabbing the first threshold table found without checking dates would have silently given the wrong-era answer for the 2025 half of the question. I nearly took the "current" table (`sec-hard-threshold`, in force 2026-01-01 onward) as the answer for 2025 since it's labeled the current/definitive one in the procurement area listing — that would have been wrong; today is 2026-09-20, but the *question* is scoped to 2023 and 2025, and the legend page says explicitly "for a question dated in 2025 the answer is the middle one, not the oldest and not the current table."

The 2023 table (`threshold-table`) was not listed directly under /v1/regions/procurement — it only appeared two hops deeper, under /v1/nodes/purchase-request → /v1/nodes/approval-threshold. The procurement table's blurb ("older pages on both subjects are still here") is misleading on its face since the oldest threshold page isn't actually in that table's own listing.

The 2024-07-01→2025-12-31 table (`hard-threshold-v2`) was the confusing part: it presents amounts as a 4×4 matrix (categories C1–C4 by bands V1–V4) with oddly specific numbers (e.g. 5,001 / 5,005 / 5,009 / 5,013 thousand KRW) and never states which role (team lead/division head/CEO) attaches to which band — it just says those figures "followed the approval thresholds rule unchanged." That forced inferring the role by matching the new V1–V2 band's position against the original table's 500,000–3,000,000 (division head) band, and separately checking that 2,000,000 KRW lands inside V1–V2 for all four categories (since the question never specifies a spend category) before trusting that the role is category-independent here. If the 2,000,000 figure had landed in different bands depending on category, this would have been unanswerable without more information — flagging that as the near-miss: don't assume a category-blind question has a category-blind answer without checking all categories against the actual thresholds first.
