## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/nodes/sec-approvals-that-move-money
./bench/rmcli.py table /v1/nodes/sec-the-approval-behind-a-purchase
./bench/rmcli.py table /v1/nodes/approval-line
./bench/rmcli.py table /v1/nodes/delegated-approval
./bench/rmcli.py read /v1/nodes/delegation-scope/body
./bench/rmcli.py table /v1/nodes/doc-admin
./bench/rmcli.py table /v1/nodes/sec-signing-authority-for-outside-parties
./bench/rmcli.py table /v1/nodes/sec-policy-and-its-own-lifecycle
./bench/rmcli.py table /v1/nodes/sec-chains-and-consent
./bench/rmcli.py table /v1/nodes/sec-delegation-in-practice
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py read /v1/nodes/threshold-table/body

## Answer

Two versions are needed, one per claim year:

**2023 claim** → the oldest approval-threshold table (in force until 2024-07-01), indexed by amount only:
- Under 500,000 KRW → Team lead, delegated (1 quote)
- 500,000 – 3,000,000 KRW → Division head, delegated (2 quotes)
- 3,000,000 – 10,000,000 KRW → CEO (3 quotes)
- 10,000,000 KRW and over → CEO, with a separate proposal (3 quotes plus a comparison)

This maps directly onto the underlying (undated, still-current-for-that-period) delegation scope: Team lead spend under 500,000 KRW; Division head spend under 3,000,000 KRW; CEO spend of 3,000,000 KRW and over.

**2025 claim** → the second version (in force 2024-07-01 to 2025-12-31), which adds spend category as a second qualifier. Thresholds became category-specific (KRW, thousands):

| category | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| C1 | 1,000 | 5,001 | 20,002 | 100,003 |
| C2 | 1,004 | 5,005 | 20,006 | 100,007 |
| C3 | 1,008 | 5,009 | 20,010 | 100,011 |
| C4 | 1,012 | 5,013 | 20,014 | 100,015 |

Who signs, quote count, and turnaround are not restated in this version — the document says they "followed the approval thresholds rule unchanged until 2026-01-01," i.e. the same Team lead / Division head / CEO structure from the delegation scope above still governs, just applied against these new category-specific amount bands rather than one flat band.

## Source
- /v1/nodes/hard-threshold-legend-revision/body (confirms which version answers a 2023-dated vs. 2025-dated question)
- /v1/nodes/threshold-table/body (2023 answer — thresholds/signers by amount, in force until 2024-07-01)
- /v1/nodes/delegation-scope/body (underlying delegation limits: Team lead / Division head / CEO)
- /v1/nodes/hard-threshold-v2/body (2025 answer — thresholds by category and amount, in force 2024-07-01 to 2025-12-31)

## Notes
- The two versions needed are not next to each other in the tree. `hard-threshold-v2` and the current `sec-hard-threshold` are both listed directly under `/v1/regions/procurement`, but the oldest version (`threshold-table`) is not — it only surfaces two hops deeper, under `purchase-request` → `approval-threshold`. If you stop at the procurement table's listing you'd conclude only two versions exist and might wrongly treat `hard-threshold-v2` as the floor for "old."
- The legend page (`hard-threshold-legend-revision`) explicitly warns that for a 2025-dated question "reaching for the newest is wrong" — the instinct to grab `sec-hard-threshold` (current, 2026-01-01 onward) for a 2025 claim is exactly the trap it calls out. Read that page before picking a version, not after.
- `threshold-table` itself carries no date or supersession notice — the legend page says as much ("the oldest says nothing at all about having been replaced"). Read on its own, it looks perfectly current; only the separate legend page tells you it stopped applying 2024-07-01.
- `hard-threshold-v2`'s section is headed "Who signs it, by category and amount" but the table under that heading is entirely KRW thresholds, not signer names or titles — it's easy to misread those figures as the signers. The actual signer answer for 2025 has to be pulled from the delegation scope in the *approval* region (a different top-level area than procurement), via a cross-reference sentence ("followed the approval thresholds rule unchanged") rather than a table.
- `delegation-scope` (the Team lead / Division head / CEO limits) lives under Approval, not Procurement, and is itself unversioned/undated but is flagged elsewhere (`hard-moved-threshold`) as "the old rule, correct only before 2026-01-01" — so it's usable for both 2023 and 2025 but not for anything dated 2026 or later.
