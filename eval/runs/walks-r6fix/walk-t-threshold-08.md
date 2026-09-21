## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py table /v1/regions/approval
    ./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
    ./bench/rmcli.py table /v1/regions/procurement
    ./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
    ./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

## Answer

The approval threshold has been written three times, and which one applies depends on the claim's date:

- Until 2024-07-01: the oldest rule (`threshold-table`, in approval), indexed by one qualifier — no longer correct.
- 2024-07-01 to 2025-12-31: the second version (`hard-threshold-v2`, in procurement), indexed by category and amount.
- From 2026-01-01: the current table (`sec-hard-threshold`, in procurement), indexed by category, amount, and term.

A claim dated in 2025 falls in the middle window, so `hard-threshold-v2` is the version that applies. Its table (amounts in thousand KRW, by category C1–C4 and tier V1–V4):

| category \ amount | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| C1 | 1000 | 5001 | 20002 | 100003 |
| C2 | 1004 | 5005 | 20006 | 100007 |
| C3 | 1008 | 5009 | 20010 | 100011 |
| C4 | 1012 | 5013 | 20014 | 100015 |

Who signs, how many quotes are needed, and turnaround time (beyond the amount column above) follow the approval thresholds rule unchanged for this window.

## Source

- /v1/nodes/hard-moved-threshold/body — found via approval region; explains the 2026-01-01 move and points to the three-version history
- /v1/nodes/hard-threshold-v2/body — the actual figures for the 2024-07-01 to 2025-12-31 window (procurement region)
- /v1/nodes/hard-threshold-legend-revision/body — full version table confirming 2025 maps to `hard-threshold-v2`

## Notes

The approval region table itself hints strongly at the trap: it says spend thresholds "moved to procurement on 2026-01-01" and that "what is still here is the old rule" — easy to misread as "old rule = 2025's rule," which is wrong. The `hard-moved-threshold` document in approval is explicit that the pages still sitting in approval are the *oldest* version, correct only before 2024-07-01, and that they were never marked as superseded even though they stopped being correct eighteen months before the 2026-01-01 move. If I'd stopped at the approval region and read only the threshold table sitting there, I'd have given the pre-2024-07-01 numbers for a 2025 claim — wrong on two counts (wrong version, and it lacks the category/amount structure the 2025 rule uses). The real answer required following the pointer into procurement to `hard-threshold-v2`, and the legend-revision page there was the one that stated outright, without me having to infer it, that "for a question dated in 2025 the answer is the middle one, not the oldest and not the current table." Also had to be careful not to grab `sec-hard-threshold` (the current, 2026-01-01-onward table) just because it's labeled "THE CURRENT APPROVAL THRESHOLD TABLE" in the procurement listing — current is not what a 2025 date needs.
