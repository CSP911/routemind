1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py overlay create --question "Junior analyst, Dhaka, 4 nights: hotel per-night cap and receipt threshold?" --member /v1/nodes/sec-hard-perdiem "current overseas per-diem table by grade/band/length of stay, in force since 2026-01-01 — has the hotel cap" --member /v1/nodes/evidence "what has to be attached for a spend to be accepted — likely has the receipt threshold" --member /v1/nodes/hard-perdiem-legend-revision "warns per-diem has three versions with different dates; need to confirm which applies"
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body
./bench/rmcli.py table /v1/nodes/qualified-evidence
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/sec-hard-perdiem/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_85a17f --address /v1/nodes/evidence --why "receipt threshold for this trip is given directly in the per-diem row itself; the general evidence-qualification table answers a different question (document type, not whether a receipt is needed)"
./bench/rmcli.py overlay close --id ov_2026-09-21_85a17f --outcome answered --used /v1/nodes/hard-perdiem-legend-revision/body /v1/nodes/hard-perdiem-legend-grade/body /v1/nodes/hard-perdiem-legend-band/body /v1/nodes/hard-perdiem-legend-stay/body /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body

2. **Answer**: Lodging cap: 147 USD per night. Receipt threshold: 48 USD (above this amount the receipt must be kept/produced). This is from the current overseas per-diem table (in force 2026-01-01 onward), grade G1 (junior analyst) × band B4 (Dhaka) × stay S2 (four nights). That row also lists meals at 85 USD/day and incidentals at 17 USD/day, not asked for here.

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (confirms the 2026-01-01 table is the version in force for a 2026-09-21 question)
/v1/nodes/hard-perdiem-legend-grade/body (junior analyst → grade G1)
/v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
/v1/nodes/hard-perdiem-legend-stay/body (four nights → stay S2)
/v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s2/body (lodging cap 147 USD/night, receipt threshold 48 USD)

4. **Notes**:
- The biggest trap here is the three overlapping versions of the overseas per-diem doc (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the legend page explicitly warns the oldest "says nothing at all about having been replaced" — so a naive read of the oldest node alone would look complete and be wrong. Today's date (2026-09-21) puts this squarely in the current table, but I checked the revision-legend explicitly rather than assuming "newest is right."
- I initially added `/v1/nodes/evidence` to the working set expecting a separate general "receipt required above X" rule, since the question phrasing ("above what amount do I have to keep the receipt") sounds like the generic evidence-qualification rule (tax invoice vs. simple receipt ceiling) rather than a per-diem field. It turned out the per-diem row itself carries a "Receipt threshold" figure that directly answers this, and the `qualified-evidence` table's "ceiling on a simple receipt" is a different concept (which document format qualifies, not whether a receipt is needed at all). I removed `evidence` from the overlay rather than use it, to avoid conflating the two.
- The three-qualifier lookup (grade/band/stay) is easy to get wrong if you skip the legends and guess codes — the legends say plainly they are "the only place the mapping is written down," so I resolved all three before opening a row rather than guessing G1/B4/S2 from pattern.
- Minor tool friction: `overlay close --used` reported the five row addresses as "reached ... from somewhere the overlay never named" rather than plain hits, because I never ran `overlay add` for the individual legend/row files — I only read them directly once the parent table (`sec-hard-perdiem`) was a member. The close still recorded them fine, but the working set as literally defined (three top-level members) didn't itself contain the specific addresses I ended up citing.
