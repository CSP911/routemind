1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/nodes/sec-approvals-that-move-money
./bench/rmcli.py table /v1/nodes/approval-line
./bench/rmcli.py table /v1/nodes/delegated-approval
./bench/rmcli.py read /v1/nodes/delegation-scope/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
```

2. **Answer**

For a claim dated anywhere in 2025, the "approval threshold" subject has been written three
times, and the version in force for 2025 (2024-07-01 through 2025-12-31) is the second one,
`hard-threshold-v2`:

| category \ amount | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| C1 | 1,000 thousand KRW | 5,001 thousand KRW | 20,002 thousand KRW | 100,003 thousand KRW |
| C2 | 1,004 thousand KRW | 5,005 thousand KRW | 20,006 thousand KRW | 100,007 thousand KRW |
| C3 | 1,008 thousand KRW | 5,009 thousand KRW | 20,010 thousand KRW | 100,011 thousand KRW |
| C4 | 1,012 thousand KRW | 5,013 thousand KRW | 20,014 thousand KRW | 100,015 thousand KRW |

This is not the pre-2024-07-01 table (`threshold-table`) and not the current, post-2026-01-01
table (`sec-hard-threshold`) — both are explicitly wrong for a 2025 date.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body — establishes that there are three versions and which date range each covers
- /v1/nodes/hard-threshold-v2/body — the actual table in force 2024-07-01 to 2025-12-31, used for the figures above

4. **Notes**

I nearly landed on the wrong answer. The `approval` region's own table blurb says spend
thresholds "moved to procurement on 2026-01-01," which pointed me to
`/v1/nodes/hard-moved-threshold/body`. That page frames the change as a simple two-era split
(before/after 2026-01-01) and names `/v1/nodes/delegation-scope/body` as "the old rule, correct
only before 2026-01-01." I followed that down through `approval-line` → `delegated-approval` →
`delegation-scope` and read a table of delegated signing authority by role (team lead / division
head / CEO). That is a real, correctly-dated document, but it is not what the question is asking
about — the question asks about the "approval threshold" (by category/amount/term), which is a
different subject that actually lives in procurement, not approval. Stopping there would have
given a plausible but wrong answer.

The real complication only shows up once you're in `/v1/regions/procurement` and read
`hard-threshold-legend-revision/body`: the "approval threshold" subject was written three
times (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), not two, and the page is
explicit that reaching for either the oldest or the current table is wrong for a 2025 date — only
the middle one applies. The `hard-moved-threshold` page in the approval region only describes a
two-era split because it's talking about a different, simpler fact (that thresholds moved out of
the approval region entirely), not the versioning within procurement's own threshold tables.

One thing that worked in my favor: the question only says "2025" with no specific month. The
middle version's range (2024-07-01 to 2025-12-31) happens to cover the entire calendar year 2025,
so there was no need to pin down an exact date — any 2025 date lands in the same version.

I did not open `/v1/nodes/threshold-table` (pre-2024-07-01) or `/v1/nodes/sec-hard-threshold`
(current, 2026-01-01 onward) since the legend-revision page already ruled both out for a 2025
date.
