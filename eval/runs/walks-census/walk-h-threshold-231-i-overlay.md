1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, about 40 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount-based approval threshold and quote requirements are likely here" --member /v1/regions/expense "travel/flights/hotels could be treated as travel expense rules"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_49b522 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body

2. **Answer**:
Signature required: the division director.
Quotes required: three competing quotes plus a written comparison.
(Delegation limit for this row is 100,045 thousand KRW; expect 12 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body

4. **Notes**:
"Flights and hotels" maps directly to category C3 in the legend, so no ambiguity there. The only judgment call was the amount band: "about 40 million won" matches "amount V4" in the legend almost verbatim, so no rounding/nearest-entry guess was needed. Same for term: "renewing every year" maps exactly to term M2 ("renewing every year").

One thing worth flagging: the table listing (`sec-hard-threshold`) carries a warning that approval threshold has had three versions over time (`hard-threshold-legend-revision`), with `hard-threshold-v2` covering 2024-07-01 to 2025-12-31 and an older `threshold-table` before that. I did not open the revision-legend or the superseded v2 table because `sec-hard-threshold` is explicitly labeled "in force from 2026-01-01" and today's date (2026-09-21) falls inside that period, so the current table was clearly the right one — but it would be easy to grab the wrong version's row if you didn't notice the effective-date label, since the row addresses across versions look almost identical (only the node prefix differs, e.g. `hard-threshold-row-...` vs a v2-prefixed equivalent). Also, the overlay's `procurement` member paid off; the `expense` member (travel expense rules) was a plausible alternate guess since flights/hotels are travel-related, but the question's real subject was an annual purchasing commitment and its approval chain, not an individual reimbursable trip expense, so procurement was correct and expense was never needed.
