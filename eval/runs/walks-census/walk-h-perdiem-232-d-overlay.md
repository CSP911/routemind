1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G3, band B4, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely holds hotel nightly cap" --member /v1/nodes/evidence "evidence table - may hold the receipt threshold amount" --member /v1/nodes/hard-perdiem-legend-revision/body "warns of three per-diem versions with different dates - need to confirm which is current for stay length definitions"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6f35af --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body

2. **Answer**: Lodging cap is 279 USD per night. The receipt threshold is 59 USD — spend above that amount requires a receipt to be kept.

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body

4. **Notes**: The expense area table flagged that overseas per-diem has three versions (a legend-revision warning), which made me add /v1/nodes/hard-perdiem-legend-revision/body and /v1/nodes/sec-hard-perdiem to the working set defensively before knowing the exact row existed. That caution turned out unnecessary once the overlay table itself printed the exact row for G3/B4/S3 directly (address `hard-perdiem-row-grade-g3-band-b4-stay-s3`) — its own body confirms it is the version "in force from 2026-01-01," which covers today (2026-09-21), so no cross-check against the superseded `hard-perdiem-v2` or `overseas-rates` versions was needed. The row also already contains both the "Lodging, per night" and "Receipt threshold" fields together, so the separate `/v1/nodes/evidence` member (added on the guess that receipt-threshold info would live in a general evidence table) was never actually used — the per-diem row is self-contained and is the more specific, correct source. Worth noting for future walks: don't assume receipt-threshold figures live in the generic evidence/qualifying-evidence table — check the specific per-diem row first, since it can carry its own threshold that overrides the general one.
