1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "March 2025: delegation limit / signer for category C2 spend, amount band V2, under threshold version in force on that date" --member /v1/regions/procurement "approval threshold by category/amount/term lives here"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e84406 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-v2/body

2. **Answer**: 5005 thousand KRW — the delegation limit for category C2, amount band V2, under the approval threshold version in force from 2024-07-01 to 2025-12-31 (which covers March 2025). No separate named signer is given in this table; it lists only the category × amount-band threshold figures, so the delegation-limit amount is the answer available.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (established which of the three threshold versions applies to a March 2025 date)
- /v1/nodes/hard-threshold-v2/body (the version in force 2024-07-01 to 2025-12-31; contains the C2 × V2 = 5005 thousand KRW figure)

4. **Notes**: The overlay's opening table surfaced both `hard-threshold-v2` (superseded) and `sec-hard-threshold` (current, in force from 2026-01-01) side by side, with no dates visible in the row descriptions beyond "SUPERSEDED" and "CURRENT" tags — grabbing the one labeled "current" would have been the wrong, and tempting, move for a March 2025 question. The legend-revision page made the actual cutover explicit (three versions: pre-2024-07-01, 2024-07-01–2025-12-31, 2026-01-01 onward) and confirmed the middle version is correct here. Worth flagging: the v2 document's own header claims "Who signs it, by category and amount," but the table beneath it only ever gives KRW amount thresholds — there is no signer name/role in this document at all, so the "who signed" half of the question is genuinely unanswerable from this source, only the delegation-limit amount is.
