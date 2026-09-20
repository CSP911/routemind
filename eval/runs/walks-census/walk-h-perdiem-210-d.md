1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body

2. **Answer**: Lodging (hotel) cap is 239 USD per night. A receipt is required above 35 USD (the receipt threshold). This is from the current overseas per-diem table, in force from 2026-01-01, which applies to today's date (2026-09-20).

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g3-band-b2-stay-s1/body

4. **Notes**: The expense area's table listing flagged upfront that overseas per-diem has three versions (a warning at /v1/nodes/hard-perdiem-legend-revision/body) — an older, superseded band-only-cap table and a 2024-07-01–2025-12-31 version (`hard-perdiem-v2`) both still exist alongside the current one (`sec-hard-perdiem`, in force since 2026-01-01). It would be easy to grab the wrong version if you didn't notice the table listing explicitly marking `sec-hard-perdiem` as "THE CURRENT" one and confirm today's date falls after its 2026-01-01 start. The G3/B2/S1 row address was printed directly by the table (grade, band, and stay codes all matched the question's terms exactly), so no legend lookup was needed for this particular question — but that's only because the question already used the row's own vocabulary (G3, B2, S1); a question phrased in plain terms (job title, destination city, trip length) would have required the three legend files first.
