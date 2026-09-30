1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G3, band B3, stay S4, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per-night caps and receipt threshold live in the expense region"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_9bdf5d --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body

2. **Answer**:
Lodging cap: 267 USD per night. Receipt required above 53 USD (the receipt threshold).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three overseas per-diem versions applies for today's date)
/v1/nodes/sec-hard-perdiem (current table, 2026-01-01 onward, located the specific row)
/v1/nodes/hard-perdiem-row-grade-g3-band-b3-stay-s4/body (the figures)

4. **Notes**:
The expense region table lists two other per-diem documents (`hard-perdiem-legend-revision` and `hard-perdiem-v2`) alongside `sec-hard-perdiem`, and `hard-perdiem-v2` is explicitly flagged SUPERSEDED. It would have been easy to grab the wrong version if the question's date weren't checked — the legend-revision doc spells out that this subject has been written three times, each covering a different date range, and that the oldest version says nothing about being replaced. Today is 2026-09-21, which falls in the 2026-01-01-onward range, so `sec-hard-perdiem` (three qualifiers: grade, band, stay) is correct. Also worth noting: the row document only gives the lodging cap and receipt threshold as asked, but it also carries meal ($99/day) and incidentals ($20/day) figures not requested here, plus a rule that an unapproved excess over the nightly lodging cap is not recoverable — not part of the question, so left out of the answer above.
