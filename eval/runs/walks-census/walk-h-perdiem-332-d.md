1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body

2. Answer
Lodging (hotel) cap: 343 USD per night.
Receipt threshold: 63 USD — above this amount a receipt must be kept.
(For context, also on this row: meals 117 USD/day, incidentals 24 USD/day.)

3. Source
/v1/nodes/hard-perdiem-legend-revision/body (confirmed which per-diem version is in force for today's date)
/v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body (the figures)

4. Notes
The expense area's table listing flags up front that overseas per-diem has three versions
(overseas-rates, hard-perdiem-v2, sec-hard-perdiem) covering different date ranges, and warns
that reaching for the newest is wrong for dates before 2026-01-01. Today is 2026-09-20, which
falls under the current table (sec-hard-perdiem, in force from 2026-01-01), so that was the
correct one to use — but it would have been easy to skip the legend-revision check and just
grab the first per-diem-looking table without confirming the date range applied. The
grade/band/stay row itself (g4-b4-s3) matched the question's parameters exactly, so no
interpretation or legend lookup for grade/band/stay codes was needed — the row was addressed
directly from the sec-hard-perdiem table listing.
