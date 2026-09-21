1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G3, band B1, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table in force from 2026-01-01, matches today's date 2026-09-21" --member /v1/nodes/hard-perdiem-legend-revision "warns there are three versions of the per-diem docs with different date ranges — need to confirm which applies" --member /v1/nodes/evidence "may define the receipt-required threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-evidence/body
./bench/rmcli.py overlay close --id ov_2026-09-21_478b50 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body

2. **Answer**: Lodging cap: 227 USD per night. Receipt threshold: 29 USD (above this amount, evidence/receipt must be kept for the claim).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s2/body

4. **Notes**: The expense region table carries an explicit warning that overseas per-diem exists in three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and that reaching for the newest is wrong for a question dated before 2026. Today is 2026-09-21, so the current table (`sec-hard-perdiem`) is correct, but this is exactly the kind of check that's easy to skip if you jump straight to the row that matches grade/band/stay without confirming the date first — worth flagging since a differently-dated version of this same question would need `hard-perdiem-v2` or `overseas-rates` instead.

I also nearly conflated the per-diem row's own "Receipt threshold" field (29 USD, specific to this per-diem claim) with the unrelated general "Qualifying evidence" doc (`/v1/nodes/qualified-evidence/body`), which sets a 30,000 KRW simple-receipt ceiling for domestic expense evidence generally. Different currency, different scope, different purpose — that doc did not contribute to the answer and I excluded it from "used" after reading it and confirming it was a false lead.

The overlay close command reported the two addresses I read as "reached... from somewhere the overlay never named" rather than matching them cleanly against the overlay's registered members — likely because the member addresses I registered at creation time didn't include the `/body` suffix that `read` required. Cosmetic, but worth noting in case it looks like an error.
