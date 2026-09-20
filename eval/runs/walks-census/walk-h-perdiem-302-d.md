## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3/body

## Answer
Lodging (hotel), per night: 295 USD
Receipt threshold: above 36 USD a receipt must be kept

## Source
/v1/nodes/hard-perdiem-row-grade-g4-band-b1-stay-s3/body

## Notes
The path was direct and unambiguous: /v1/regions/expense listed /v1/nodes/sec-hard-perdiem explicitly as "THE CURRENT OVERSEAS PER-DIEM TABLE, in force from 2026-01-01," so there was no need to touch the superseded `hard-perdiem-v2` or `overseas-rates` versions. The table under sec-hard-perdiem is indexed by grade/band/stay code directly in the address (hard-perdiem-row-grade-g4-band-b1-stay-s3), so the G4/B1/S3 combination from the question mapped straight onto one row with no legend lookup needed. The row itself contains both figures asked about (lodging per night and receipt threshold) in one table, so a single read sufficed — no need to cross-check the general /v1/nodes/evidence table, since this row's "Receipt threshold" field is more specific to this per-diem context than a general evidence rule would be.
