1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Team manager, Dhaka, 8 nights - hotel per-night cap and receipt threshold" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, likely has hotel cap by night" --member /v1/nodes/evidence "receipt requirement threshold likely defined here" --member /v1/nodes/hard-perdiem-legend-revision/body "warns which per-diem version covers which dates"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f1b54b --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body

2. **Answer**: Lodging cap is 215 USD per night. The receipt threshold is 55 USD — above that amount a receipt must be kept (below it, none is required for this line).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body

4. **Notes**: Three near-misses. First, the expense area lists three different overseas per-diem documents (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) covering different date ranges, and the legend-revision doc warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01 — today (2026-09-21) is inside the current table's range, so `sec-hard-perdiem` was correct, but this is exactly the kind of question where grabbing the wrong version silently gives a plausible-looking wrong number. Second, the per-diem row is selected by three separate legend lookups (grade from job title, country band from city, stay band from night count) that must each be resolved before the right of ~64 leaf rows can be addressed — "team manager" maps to G2, not G1 (G1 is "a junior analyst"), which is easy to get wrong if you guess grade by seniority-sounding intuition instead of using the legend table. Third, there is a second, unrelated "receipt threshold" concept in this domain: `/v1/nodes/qualified-list/body` gives a general domestic evidence rule denominated in KRW (30,000 KRW threshold, tax-invoice requirements, etc.) that looked like a strong candidate from the region table's description ("the ceiling on a simple receipt") but turned out to be a different policy (domestic expense evidence, not overseas per-diem). The per-diem row itself carries its own "Receipt threshold" field (55 USD) which is the one that actually answers this question — I checked the KRW doc to rule it out rather than assume, and it does not apply here.
