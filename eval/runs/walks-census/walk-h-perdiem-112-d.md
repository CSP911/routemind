1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s3/body

2. **Answer**:
Lodging cap: 183 USD per night. Receipt threshold: 37 USD (a receipt must be kept for any spend above this amount). (For reference, the same row also gives meals at 71 USD/day and incidentals at 14 USD/day.)

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s3/body

4. **Notes**:
The expense area lists three versions of the overseas per-diem: the current table (`sec-hard-perdiem`, in force from 2026-01-01), a superseded `hard-perdiem-v2` (2024-07-01 to 2025-12-31), and an older `overseas-rates`. Today's date (2026-09-20) falls under the current table, so `sec-hard-perdiem` was the correct one to open — it would have been easy to grab the superseded v2 node by mistake since it also appeared directly in the expense area listing. The row address itself directly encodes grade/band/stay (grade-g2-band-b2-stay-s3), so no ambiguity once inside the table — it was a straight lookup, no legend translation needed since the question was already given in G2/B2/S3 codes.
