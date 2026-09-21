1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G4, band B3, stay S2, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force since 2026-01-01" --member /v1/nodes/hard-perdiem-legend-revision "warns of three versions of the per-diem table, need to confirm which is current for today's date" --member /v1/nodes/evidence "may hold the receipt-required threshold"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f04a3b --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap is 323 USD per night. A receipt has to be kept for any spend above 51 USD (the receipt threshold). (For reference, this row also gives meals at 98 USD/day and incidentals at 20 USD/day, in force from 2026-01-01, current for today's date of 2026-09-21.)

3. **Source**:
- /v1/nodes/hard-perdiem-row-grade-g4-band-b3-stay-s2/body (lodging cap, receipt threshold)
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed this version, in force 2026-01-01 onwards, is the correct one for today's date)

4. **Notes**:
The expense area table flagged upfront that overseas per-diem has three superseded versions layered in the same area (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), with an explicit warning that reaching for the newest is wrong for a question dated before 2026-01-01. I added the legend-revision page to the working set from the start specifically to check this before trusting the current table, since the older versions apparently don't self-identify as superseded. That turned out to be exactly right — the legend confirms 2026-09-21 falls under the current table (`sec-hard-perdiem`, 2026-01-01 onwards), so no correction was needed, but skipping that check would have been an easy way to get a right-looking answer for the wrong reason. I initially also added the `evidence` table as a member, expecting the receipt threshold might live there separately from the per-diem row, but the per-diem row itself already carried a "Receipt threshold" field, so that member was never needed — good thing to note since a less careful pass might have gone hunting through the evidence table for a number that was already sitting in the row.
