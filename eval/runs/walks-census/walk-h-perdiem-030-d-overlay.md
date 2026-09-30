1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For grade G1, band B4, stay S1, what can I put on a hotel each night, and above what amount do I have to keep the receipt?" --member /v1/regions/expense "hotel per-night cap and receipt threshold are travel expense topics"
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_0cc676 --outcome answered --used /v1/nodes/sec-hard-perdiem /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body

2. **Answer**:
Lodging cap: 143 USD per night. Receipt required above 45 USD (the receipt threshold).

3. **Source**:
/v1/nodes/sec-hard-perdiem (table, to locate the row) → /v1/nodes/hard-perdiem-row-grade-g1-band-b4-stay-s1/body (the figures)

4. **Notes**:
The overlay's opening table under /v1/regions/expense surfaced two decoys worth flagging: `hard-perdiem-v2` (explicitly labeled SUPERSEDED, covering 2024-07-01 to 2025-12-31) and a `hard-perdiem-legend-revision` warning that overseas per-diem has three versions with different figures. It would be easy to grab a number from the wrong version. `sec-hard-perdiem` is explicitly labeled "in force from 2026-01-01" and today is 2026-09-21, so it's the current table and the one to use — no need to consult the older versions or the legend-revision note further. The grade/band/stay row structure was exact and unambiguous (grade-g1-band-b4-stay-s1 matched the question's G1/B4/S1 directly), so no legend lookups were needed to translate a job title or destination into codes. The overlay close reported the two addresses I named in `--used` as "reached" rather than tracked members — that's just because I never ran `overlay add` for them before closing (they came from following the table listing rather than an explicit add); the answer itself is unaffected.
