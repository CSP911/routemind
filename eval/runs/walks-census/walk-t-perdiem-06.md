1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body

2. **Answer**: 115 USD (grade G2, band B2, nightly lodging cap, under the 2024-07-01 to 2025-12-31 version of the overseas per-diem).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established that August 2025 is covered by the "v2" version, not the oldest or current table)
- /v1/nodes/hard-perdiem-v2/body (the table itself, G2 × B2 = 115 USD)

4. **Notes**: The expense table's own description flags that "the older band-only caps are still here and are superseded," which nudges toward just grabbing the current table (`sec-hard-perdiem`) — that would have been wrong for a 2025 date. The legend-revision doc was the key check: it explicitly warns that reaching for the newest table is wrong for anything before 2026-01-01, and that the oldest version (`overseas-rates`) says nothing about being replaced, so an ungrounded read could easily land on the wrong one silently. Confirming the in-force window (2024-07-01 to 2025-12-31) against the question's date (August 2025) before reading the actual figures avoided that mistake.
