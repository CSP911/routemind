1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In September 2023, what screening was required for a new supplier? Under the version of supplier due diligence in force on that date." --member /v1/regions/procurement "supplier due diligence is likely a procurement policy topic"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py overlay add --id ov_2026-09-20_befef7 --address /v1/nodes/supplier-due-diligence/body --why "this is the version in force until 2024-07-01, which covers Sept 2023, per the legend revision page"
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py overlay close --id ov_2026-09-20_befef7 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/supplier-due-diligence/body

2. **Answer**
Under the version of supplier due diligence in force in September 2023 (the oldest version, in force until 2024-07-01), a new supplier had to pass three checks before registration:
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen (whether the entity or its owners had been flagged before)
A sanctions hit or a refused code of conduct stopped registration outright, with no delegated sign-off able to override it.

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (established that the pre-2024-07-01 version, at /v1/nodes/supplier-due-diligence/body, is the one that covers September 2023)
- /v1/nodes/supplier-due-diligence/body (the actual screening requirements)

4. **Notes**
The procurement table surfaces three parallel supplier-due-diligence documents (the oldest, a "v2" superseded one, and the current "sec-hard-diligence" one) with no date in their titles alone — picking the current or newest-looking one instead of checking the legend page would have been the wrong answer here, since September 2023 predates all of the versioned revisions. The legend page explicitly warns that "the oldest says nothing at all about having been replaced," which is exactly the trap: nothing on the oldest document itself tells you it's superseded, so without deliberately reading the legend first, it would look like the current, universally-applicable policy. Also worth noting: the oldest document's address is plain `supplier-due-diligence`, not prefixed `hard-diligence-` like the two later versions — it wasn't in the first overlay table until I went one level deeper via the `sec-supplier-due-diligence` "where to start" table to find its exact address.
