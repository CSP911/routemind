1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "For grade G4, band B2, stay S3, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/stay, in force from 2026-01-01 - matches the question's grade/band/stay format" --member /v1/nodes/hard-perdiem-legend-revision/body "warns there are three versions of the per-diem table with different dates - need to confirm which is current for today 2026-09-21" --member /v1/nodes/evidence "evidence/receipt table - likely has the receipt threshold amount"
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py read /v1/nodes/qualified-list/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8e7c3c --outcome answered --used /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**:
Lodging cap: 311 USD per night. Receipt required above 45 USD (the receipt threshold for this row).

3. **Source**:
- /v1/nodes/hard-perdiem-row-grade-g4-band-b2-stay-s3/body (lodging cap and receipt threshold figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed this current table, in force from 2026-01-01, is the correct version for today's date, 2026-09-21, since no other date was given in the question)

4. **Notes**:
The expense area's table listing warned upfront that overseas per-diem has three versions with different in-force dates, and that reaching for the newest is wrong for a question dated before 2026-01-01. This question carries no date of its own, so I checked the revision legend explicitly rather than assuming — today (2026-09-21) falls after 2026-01-01, so the current table (`sec-hard-perdiem`) is correct, not `hard-perdiem-v2` or the oldest `overseas-rates`.

The near-miss: I also pulled the general "qualified evidence" table (`/v1/nodes/qualified-evidence` → `qualified-list/body`), expecting it might hold the receipt threshold the question was asking about. It turned out to be a different, domestic-context rule quoted in KRW (simple receipt fine up to 30,000 KRW, qualifying evidence required above that) — unrelated to the USD-denominated overseas per-diem row. The per-diem row itself already carries its own "Receipt threshold" field (45 USD), which is the actual answer. It would have been easy to conflate the two thresholds or to cite the KRW figure by mistake since both tables use the word "receipt" — the per-diem row is self-contained and is the one that answers this question.
