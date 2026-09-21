1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Managing director, Dhaka, eight nights: hotel per-night cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay length, likely has hotel cap" --member /v1/nodes/hard-perdiem-legend-revision "warns per-diem has 3 versions with different dates, need to confirm which applies" --member /v1/nodes/evidence "receipt requirement threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-evidence/body
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_bf8da1 --address /v1/nodes/evidence --why "qualified-evidence/qualified-list turned out to be domestic KRW receipt-evidence rules (30,000 KRW threshold), unrelated to the overseas per-diem receipt threshold already given in the per-diem row itself"
./bench/rmcli.py overlay add --id ov_2026-09-21_bf8da1 --address /v1/nodes/hard-perdiem-legend-grade/body --why "confirms managing director = grade G4"
./bench/rmcli.py overlay add --id ov_2026-09-21_bf8da1 --address /v1/nodes/hard-perdiem-legend-band/body --why "confirms Dhaka = band B4"
./bench/rmcli.py overlay add --id ov_2026-09-21_bf8da1 --address /v1/nodes/hard-perdiem-legend-stay/body --why "confirms eight nights = stay S3"
./bench/rmcli.py overlay add --id ov_2026-09-21_bf8da1 --address /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body --why "the actual row: G4/B4/S3 gives lodging 343 USD/night and receipt threshold 63 USD"
./bench/rmcli.py overlay close --id ov_2026-09-21_bf8da1 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body

2. **Answer**
Lodging cap: 343 USD per night.
Receipt threshold: over 63 USD you must keep the receipt.
(For reference, this row also gives meals at 117 USD/day and incidentals at 24 USD/day, and any unapproved excess over the lodging cap is not recoverable.)

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body (confirms today's date 2026-09-21 falls under the current table, sec-hard-perdiem, not the two superseded versions)
/v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
/v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
/v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
/v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s3/body (the figures: 343 USD lodging, 63 USD receipt threshold)

4. **Notes**
The one place this walk could have gone wrong is the per-diem versioning: /v1/regions/expense's table lists three overlapping per-diem documents (overseas-rates, hard-perdiem-v2, sec-hard-perdiem), and hard-perdiem-legend-revision warns explicitly that reaching for the newest is wrong for dates before 2026-01-01 and that the oldest document never says it was replaced. Today (2026-09-21) is safely inside the current table's range, so this resolved cleanly, but a claim dated in 2025 would need hard-perdiem-v2 instead — easy to get wrong if the legend page were skipped.

The other near-miss: I initially pulled /v1/nodes/evidence (qualified-evidence / qualified-list) expecting it to answer "above what amount do I have to keep the receipt," since that's literally what its own description promises. It turned out to be a domestic, KRW-denominated receipt-qualification rule (30,000 KRW simple-receipt ceiling, cash-receipt-against-company-number trap) with no connection to the overseas per-diem trip in the question. The actual receipt threshold for this Dhaka trip (63 USD) was sitting inside the per-diem row itself all along, under the plain label "Receipt threshold." Pulling in the KRW figure would have been a wrong answer dressed as a right one — same phrase ("receipt threshold"), completely different regime. I removed that member from the overlay once I confirmed it wasn't the applicable rule for this question.

The grade/band/stay lookups (legend-grade, legend-band, legend-stay) are indirection that has to be resolved before the row address can even be constructed — "managing director," "Dhaka," and "eight nights" don't appear anywhere in the per-diem row addresses themselves; they have to be translated to G4/B4/S3 first via the three legend tables.
