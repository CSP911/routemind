1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body

2. **Answer**
For grade G3, band B1, stay S3 (in force from 2026-01-01, current as of 2026-09-20):
- Lodging (hotel), per night: 231 USD
- Receipt threshold: 32 USD — you must keep the receipt for any spend above this amount.

(Also on this row, though not asked: meals 66 USD/day, incidentals 13 USD/day.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body

4. **Notes**
The expense area table flagged up front that overseas per-diem has three historical versions
(current since 2026-01-01, a superseded 2024-07-01–2025-12-31 version `hard-perdiem-v2`, and an
older `overseas-rates`), with a legend node `hard-perdiem-legend-revision` dedicated to sorting out
which dates map to which version. It would have been easy to grab a stale rate table by mistake if
I'd picked one of the superseded nodes first. I went straight to `sec-hard-perdiem`, which the region
table explicitly labels "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01," and today's
date (2026-09-20) falls inside that range, so I didn't need to open the revision-legend file to be
sure. The question gave grade/band/stay codes directly (G3, B1, S3), so I also didn't need the
grade/band/stay legend files that translate job titles, destination cities, or trip lengths into
those codes — going to them would have been wasted steps. The row address itself was predictable
once the pattern was visible, but I did not construct it — I read it verbatim from the table listing
before requesting it.
