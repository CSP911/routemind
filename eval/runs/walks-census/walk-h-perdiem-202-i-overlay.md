1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Department head, Tokyo, 8 nights: hotel per-night limit and receipt threshold" --member /v1/regions/expense "hotel spend caps and receipt requirements for business trips live here"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_3eaf84 --outcome answered --used /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body
```

2. **Answer**
Lodging cap: 231 USD per night. Receipt required above: 32 USD.
(Also on this row, though not asked: meals 66 USD/day, incidentals 13 USD/day.)
Basis: department head → grade G3, Tokyo → band B1, eight nights → stay S3, and the table in force today (2026-09-21) is the current one (effective 2026-01-01 onward).

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (department head → G3)
- /v1/nodes/hard-perdiem-legend-band/body (Tokyo → B1)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → S3)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms which of the three per-diem versions applies to today's date)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s3/body (the figures)

4. **Notes**
- Overseas per-diem has three superseded/current versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) and the oldest one says nothing about being replaced — it would look authoritative on its own. The legend-revision doc is the only thing that tells you which one applies to a given date, and it warns explicitly that "reaching for the newest is wrong for anything before 2026-01-01." Today (2026-09-21) is safely inside the current table's range, but this is exactly the kind of question where I'd want to double check the date before trusting the first row I found, especially if I'd started from a `sec-hard-perdiem` search result rather than reading the revision warning first.
- The three legends (grade, band, stay) must each be resolved before the row address can even be built — "department head," "Tokyo," and "eight nights" don't appear anywhere in the row addresses themselves (G3/B1/S3). Skipping any one of the three legends risks guessing the wrong row.
- The row also lists meal and incidental allowances I wasn't asked about; included them as an aside only, not as part of the answer, since the question was specifically about hotel/night and the receipt threshold.
