1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s4/body

2. **Answer**:
For grade G1, band B1, stay S4 (current table, in force from 2026-01-01): lodging cap is 107 USD per night. The receipt threshold is 27 USD — spend above that amount requires a receipt.

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s4/body

4. **Notes**:
The expense area table flagged that overseas per-diem has three versions (current, a 2024-07-01–2025-12-31 version `hard-perdiem-v2`, and an older `overseas-rates`), which is an easy place to grab the wrong figures. The `sec-hard-perdiem` table header itself states it's the current table in force from 2026-01-01, and today is 2026-09-20, so no need to open the legend-revision doc separately to confirm currency — but it's worth flagging that a careless walk could have opened `hard-perdiem-v2` by mistake given how similar the addresses look. The target row (grade-g1-band-b1-stay-s4) was listed directly in the sec-hard-perdiem table by exact address, so no need to consult the grade/band/stay legends to decode the codes — they were already given as G1/B1/S4 in the question.
