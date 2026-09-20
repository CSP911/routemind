1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body

2. **Answer**
For grade G1, band B1, stay S2 (current table, in force since 2026-01-01): the hotel (lodging) cap is 99 USD per night, and receipts must be kept for any single spend above 21 USD (the receipt threshold).

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g1-band-b1-stay-s2/body

4. **Notes**
The expense area's table listing flags upfront that overseas per-diem has three versions in force over different date ranges (superseded `overseas-rates`, then `hard-perdiem-v2` for 2024-07-01 to 2025-12-31, then the current `sec-hard-perdiem` table from 2026-01-01). Today's date (2026-09-20) falls under the current table, and its listing explicitly states it "replaces `overseas-rates` and the older rules around it," so I went straight to `sec-hard-perdiem` rather than the superseded nodes — but it would have been easy to grab the wrong version if the date check were skipped. The grade/band/stay codes (G1/B1/S2) were given directly in the question and matched an exact row address in the table listing, so I did not need to consult the grade/band/stay legend files to translate a job title or destination city into codes — those legends exist for cases where the qualifiers aren't already known as codes.
