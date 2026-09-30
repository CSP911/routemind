1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "In March 2025, what was the nightly lodging cap for a grade 2 traveller going to a band B2 destination? Answer under the version of the overseas per-diem that was in force on that date." --member /v1/nodes/hard-perdiem-legend-revision/body "explains which per-diem version covers which date range" --member /v1/nodes/hard-perdiem-v2/body "candidate version in force 2024-07-01 to 2025-12-31, covers March 2025" --member /v1/nodes/sec-hard-perdiem "current table from 2026-01-01, likely not applicable but keep for comparison"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_0edf55 --address /v1/nodes/sec-hard-perdiem --why "current table is 2026-01-01 onward, not applicable to March 2025 date in question"
./bench/rmcli.py overlay close --id ov_2026-09-20_0edf55 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-v2/body

2. **Answer**: 115 USD nightly lodging cap (grade G2, band B2, under the 2024-07-01 to 2025-12-31 version of the overseas per-diem).

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions covers March 2025)
- /v1/nodes/hard-perdiem-v2/body (the grade × band lodging cap table itself)

4. **Notes**: The expense area table flags up front that there are three versions of the overseas per-diem with overlapping validity, and that the current table (`sec-hard-perdiem`, effective 2026-01-01) is a trap for any date before that — it explicitly warns "reaching for the newest is wrong for anything before 2026-01-01." I initially pulled `sec-hard-perdiem` into the working set for comparison, which turned out to be the wrong table entirely (it's indexed by three qualifiers — grade, band, stay — since it adds trip length as a dimension from 2026 onward; the pre-2026 tables aren't banded by stay length at all). The legend-revision page was the key disambiguator: it states plainly that a 2025-dated question needs the *middle* version (`hard-perdiem-v2`), not the oldest (`overseas-rates`, pre-2024-07-01, which had neither grade nor stay bands) and not the current one. Worth flagging that the oldest version "says nothing at all about having been replaced" — if I'd landed on `overseas-rates` first without checking the legend page, I'd have had no in-document signal that a newer version existed. Once on `hard-perdiem-v2`, the G2/B2 cell was unambiguous: 115 USD.
