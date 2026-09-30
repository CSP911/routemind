## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py overlay create --question "A couple of laptops, around 12 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "procurement threshold by category/amount/term decides approval signer and whether competitive quotes are required"
    ./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
    ./bench/rmcli.py table /v1/nodes/sec-hard-threshold
    ./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
    ./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
    ./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
    ./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body
    ./bench/rmcli.py overlay close --id ov_2026-09-21_9d676e --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body

## Answer

The department head signs it off. Yes — three competing quotes are required before approval. (Delegation limit for this row: 20,009 thousand KRW; expect 9 working days.)

## Source

- /v1/nodes/hard-threshold-legend-revision/body
- /v1/nodes/hard-threshold-legend-category/body
- /v1/nodes/hard-threshold-legend-amount/body
- /v1/nodes/hard-threshold-legend-term/body
- /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m2/body

## Notes

The approval threshold subject has three superseded/current versions in force over different date ranges, flagged by a legend-revision page that explicitly warns the oldest version says nothing about having been replaced. Today (2026-09-21) falls after 2026-01-01, so the current table (`sec-hard-threshold`) is the right one — but it would have been easy to grab `hard-threshold-v2` (2024-07-01 to 2025-12-31) by mistake since it appeared right alongside the current one in the working set with a very similar name, and its "SUPERSEDED" label is easy to skim past. Checked the revision-legend page first specifically to avoid that trap.

All three qualifiers (category, amount, term) mapped to exact, non-fuzzy legend entries — "a couple of laptops" → C1, "around 12 million won" → V3, "renewing every year" → M2 — all worded identically to the question, so no nearest-match judgment call was needed here, unlike what the legends' fallback instructions anticipate for messier inputs.
