1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body

2. **Answer**
Hotel (lodging) cap: 215 USD per night. Receipt required for any spend above 55 USD (the receipt threshold). This is the current table, in force from 2026-01-01, which covers today's date (2026-09-20).

3. **Source**
/v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to today's date)
/v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s3/body (the figures)

4. **Notes**
The expense area table carries a loud warning that overseas per-diem has three superseded-but-not-marked-superseded versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and that reaching for the newest by default is wrong for any date before 2026-01-01. That's a real trap for a question with no date attached — I checked the legend-revision doc explicitly rather than assuming "current" was safe, since today's date (2026-09-20) is what makes `sec-hard-perdiem` correct here, not a default. The question already gave grade/band/stay codes (G2/B4/S3) rather than plain-language descriptions, so I skipped the grade/band/stay legend files — worth flagging in case that assumption is wrong and the codes needed translation from something else.
