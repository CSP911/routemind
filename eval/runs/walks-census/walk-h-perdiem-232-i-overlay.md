1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Department head, Dhaka, eight nights: hotel per-night cap and receipt threshold?" --member /v1/regions/expense "trip allowance / receipt rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_96cde4 --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body

2. **Answer**:
Lodging cap: 279 USD per night. Receipt required for any single spend above 59 USD (the receipt threshold). (For context, same row also gives meals 108 USD/day and incidentals 22 USD/day, but the question asked only about the hotel and the receipt line.)

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (established 2026-09-20/21 falls under the current table, not the two superseded versions)
- /v1/nodes/hard-perdiem-legend-grade/body (department head → grade G3)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
- /v1/nodes/hard-perdiem-legend-stay/body (eight nights → stay S3)
- /v1/nodes/hard-perdiem-row-grade-g3-band-b4-stay-s3/body (the answering row: lodging 279 USD/night, receipt threshold 59 USD)

4. **Notes**:
- This region has a real trap: the overseas per-diem subject has three superseded versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`) and the oldest version gives no indication it was replaced. Checking the revision-legend page before trusting the current table's numbers was necessary, not optional — today's date (2026-09-20/21) puts this squarely in the current table's range (2026-01-01 onward), so no ambiguity here, but it would have been easy to grab the current table without checking and get lucky rather than being right for the right reason.
- The three qualifiers (grade/band/stay) each need their own legend lookup before the row address can be built — "department head", "Dhaka", and "eight nights" are exact matches in their respective legends (G3, B4, S3), so no nearest-neighbor judgment call was needed here.
- The overlay's `close --used` accepted the legend and row addresses even though they were never added as overlay members (they came from opening `/v1/nodes/sec-hard-perdiem` as a table, one hop below the overlay's members) — the tool flagged this as "reached ... from somewhere the overlay never named" rather than rejecting it. Worth flagging: the working set as printed didn't include the actual leaf documents I ended up citing, only the section-level containers.
- The question asks "what can I put on a hotel each night" and "above what amount do I have to keep the receipt" — read literally, the second question could mean the meal/incidental receipt threshold too, but the row gives one single receipt threshold (59 USD) that applies across the claim, not a separate one for lodging, so no split was needed.
