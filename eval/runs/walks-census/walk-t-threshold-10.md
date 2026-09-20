1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
```

2. **Answer**
Delegation limit for category C2, amount band V2: **5005 thousand KRW**. This version's table does not restate who signs at that band (see Notes) — it says who signs, quote counts, and turnaround followed the original approval-thresholds rule "unchanged."

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (established 3 July 2024 falls in the 2024-07-01 to 2025-12-31 window, so the v2 table applies)
- /v1/nodes/hard-threshold-v2/body (the C2/V2 cell: 5005 thousand KRW)

4. **Notes**
The date math is the crux: "two days after the first change" only makes sense once you see the legend page — the first change to this table was 2024-07-01 (the old "threshold-table" version was superseded), so 3 July 2024 is two days into the second version (`hard-threshold-v2`), not the original or the current (2026-01-01+) table. It would have been easy to grab the current `sec-hard-threshold` table instead since it's the one flagged "CURRENT" in the procurement area listing — that would have been wrong for this date.

The table header in `hard-threshold-v2` says "Who signs it, by category and amount" but the cells actually hold KRW amounts, not names — the page explicitly states that who-signs, quote-count, and turnaround-time did not vary in this version and continued to follow the original (pre-2024-07-01) approval-thresholds rule. That original rule is referenced only by the short name `threshold-table` in the legend page, with no full address printed anywhere I was allowed to open, so I could not chase down an actual signer name for C2/V2 — I'm reporting the delegation-limit figure only, per the "delegation limit or who signed" phrasing in the question, since only one of those two was retrievable.
