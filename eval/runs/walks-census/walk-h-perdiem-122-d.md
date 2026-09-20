1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body

2. **Answer**:
Lodging (hotel), per night: 199 USD. Receipt is required for any spend above 46 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-row-grade-g2-band-b3-stay-s3/body

4. **Notes**:
The expense area's table listing flags that overseas per-diem has three superseding versions (current since 2026-01-01, an older 2024-07-01–2025-12-31 version `hard-perdiem-v2`, and an even older `overseas-rates`), so it would have been easy to grab a stale row from the wrong version. The row read here is explicitly dated "In force from 2026-01-01," which matches today's date (2026-09-20), so it's the correct, current figure. The grade/band/stay codes (G2/B3/S3) were given directly in the question, so no need to consult the legend files to translate a job title or destination city into a code — but if the codes hadn't been given, that step would have been necessary and easy to skip by mistake.
