1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In March 2023, what screening was required for a new supplier? Answer under the version of supplier due diligence in force on that date." --member /v1/regions/procurement "procurement area covers supplier onboarding/due diligence policy"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py overlay add --id ov_2026-09-20_460afa --address /v1/nodes/supplier-due-diligence/body --why "legend says pre-2024-07-01 dates (incl. March 2023) are answered by the oldest version, indexed at this address"
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py overlay close --id ov_2026-09-20_460afa --outcome answered --used /v1/regions/procurement /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/supplier-due-diligence/body

2. **Answer**:
Under the version of supplier due diligence in force in March 2023 (the oldest of three versions, in force until 2024-07-01), a new supplier had to pass three checks:
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen (has this entity or its owners been flagged before)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (established which of the three versions applies to March 2023)
- /v1/nodes/supplier-due-diligence/body (the oldest version, in force until 2024-07-01, containing the actual answer)

4. **Notes**:
The working set from /v1/regions/procurement surfaced two other supplier-due-diligence documents that look current at a glance — sec-hard-diligence ("THE CURRENT SUPPLIER DUE DILIGENCE TABLE") and hard-diligence-v2 ("SUPERSEDED... 2024-07-01..."). Neither is right for March 2023, and it would have been easy to grab sec-hard-diligence just because it's labeled "current" without checking dates. The legend document (hard-diligence-legend-revision/body) explicitly warns that this subject has three versions, that reaching for the newest is wrong for anything before 2026-01-01, and — critically — that "the oldest says nothing at all about having been replaced," so the oldest document itself gives no signal that it might not apply. Without reading the legend first, there would have been no way to know the oldest, unflagged-looking document was in fact the correct one for a 2023 date. The oldest version's address (supplier-due-diligence, no qualifier) also wasn't listed directly in the procurement area's table — it only surfaced after opening the "where to start" table (sec-supplier-due-diligence), which is a step the legend doesn't call out, so it took one extra hop to actually retrieve the right document.
