1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C2, amount V3, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, likely holds signature requirement by category/amount/term" --member /v1/nodes/purchase-request "may hold quote requirement rules" --member /v1/nodes/hard-threshold-legend-revision/body "warns of three threshold versions with different dates - need to confirm which applies"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_23339b --address /v1/nodes/purchase-request --why "exact matching row found directly in sec-hard-threshold, no need for the superseded/general purchase-request quote guidance"
./bench/rmcli.py overlay close --id ov_2026-09-21_23339b --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body

2. **Answer**
The division director signs it off, and yes — three competing quotes are required first (delegation limit 20,026 thousand KRW, 10 working days to expect).

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed the current, 2026-01-01-onwards table applies for a question dated 2026-09-21)
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body (the figures)

4. **Notes**
The procurement table's revision-legend page is a real trap here: approval threshold has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onwards), and the oldest version says nothing about being superseded — so grabbing the first C2/V3/M3-shaped row you see without checking dates could silently give you the wrong-era answer. The question carries no date of its own, so I anchored on "today" (2026-09-21, per the system date), which falls in the current-table window, making `sec-hard-threshold` → the three-qualifier row the right pick, not `hard-threshold-v2` or `threshold-table`.

The overlay table conveniently pre-expanded into every category×amount×term row under `sec-hard-threshold`, so the exact row for C2/V3/M3 was visible by name without needing the legend-category/amount/term pages to decode which band each qualifier meant — the question already gave the coded values (C2, V3, M3) directly. I never added that exact row as an overlay member before reading it, just read it straight off the printed table listing; the close command flagged it as "reached" (answered from somewhere the overlay never named) rather than a tracked member — worth noting as a quirk of the tool, not a mistake in the answer, since the address was still exactly the one printed by the table.

I initially added `/v1/nodes/purchase-request` as a candidate for the "quotes first" half of the question, worried the threshold table might only cover signatures. It didn't need it — the row itself has a "Competing quotes" field — so I removed it before closing.
