1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body

2. **Answer**
115 USD per night.

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-v2/body

4. **Notes**
"The first change" is 2024-07-01, the start of the second per-diem version (`hard-perdiem-v2`); two days after that is 2024-07-03, which falls inside that version's 2024-07-01–2025-12-31 window. The temptation to go wrong here is real: the expense area table also lists `sec-hard-perdiem` as "THE CURRENT OVERSEAS PER-DIEM TABLE," and it's tempting to grab the newest/current-looking table by default. The legend doc (`hard-perdiem-legend-revision`) exists specifically to stop that — it says three versions exist, none marked as withdrawn, and the date on the question decides which applies, warning explicitly that reaching for the newest is wrong for anything before 2026-01-01. It also confirms the middle version is indexed by grade+band only (two qualifiers), matching the question's grade 2 / band B2 lookup, whereas the current table adds stay length as a third qualifier — a good cross-check that v2 was the right table. Read the legend before the actual table, which resolved the ambiguity cleanly with no false starts.
