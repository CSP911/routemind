1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/nodes/sec-approvals-that-move-money
./bench/rmcli.py table /v1/nodes/approval-line
./bench/rmcli.py table /v1/nodes/delegated-approval
./bench/rmcli.py read /v1/nodes/delegation-scope/body
./bench/rmcli.py table /v1/nodes/purchase-request
./bench/rmcli.py table /v1/nodes/approval-threshold
./bench/rmcli.py read /v1/nodes/threshold-table/body
```

2. **Answer**
For January 2024 (pre-2024-07-01 rule, the oldest of three threshold versions), a purchase of
2,000,000 KRW net of VAT falls in the "500,000 – 3,000,000 KRW" band: **Division head approval,
delegated, 2 quotes required**. This matches the general delegation-of-authority table, which caps
a Division head's own-authority spend at "under 3,000,000 KRW" (and a Team lead's at under
500,000 KRW) — 2,000,000 KRW sits inside the Division head's delegated scope, below the point
where it would have to go to the CEO.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (established which of the three threshold versions is in force for a January 2024 date)
- /v1/nodes/hard-threshold-v2/body (pointed to `threshold-table` as the pre-2024-07-01 rule)
- /v1/nodes/hard-moved-threshold/body (pointed to `delegation-scope` as the authority rule in force before 2026-01-01)
- /v1/nodes/delegation-scope/body (delegated-authority amounts by role: Team lead / Division head / CEO)
- /v1/nodes/threshold-table/body (the actual amount-band table in force for Jan 2024, giving the answer directly)

4. **Notes**
- The trap here is reaching for the newest-looking table. `/v1/regions/procurement` foregrounds
  `sec-hard-threshold` as "THE CURRENT APPROVAL THRESHOLD TABLE" and `hard-threshold-v2` as the
  next-most-recent superseded version — neither applies to January 2024. Only the legend-revision
  page states explicitly that a *third*, older version exists and that it covers anything before
  2024-07-01, with no threshold amounts shown at that stop. Skipping that page would have produced
  a confidently wrong answer using the 2024-07-01–2025-12-31 table instead.
- The actual document for the pre-2024-07-01 rule was never listed directly under
  `/v1/regions/procurement` — its address (`threshold-table`) was only named in passing, in prose,
  inside `hard-threshold-v2`'s body, without a live link. I initially treated that as a hint rather
  than an address (per the "never construct an address" rule) and had to hunt for the real
  `/v1/nodes/...` address by walking `purchase-request` → `approval-threshold` → `threshold-table/body`
  — the name matched but the path only became a real address once a table actually printed it.
- Similarly, `delegation-scope` was named in prose inside `/v1/nodes/hard-moved-threshold/body`
  (from the `approval` region) and only became a real, followable address once printed by
  `/v1/nodes/delegated-approval`'s table.
- Two independent tables (`delegation-scope`, general authority-by-role; `threshold-table`,
  purchasing-specific amount bands) agree on the same cutover point (3,000,000 KRW) and the same
  answer (Division head) for a 2,000,000 KRW purchase, which is reassuring corroboration rather
  than redundancy — the question's "delegation limit or who signed" phrasing suggested both were
  worth checking since they could plausibly have diverged.
