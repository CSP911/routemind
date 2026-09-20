1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body
./bench/rmcli.py table /v1/nodes/evidence
./bench/rmcli.py read /v1/nodes/evidence/body
```

2. **Answer**
For a junior analyst (grade G1) on a three-week trip (stay S4) to Jakarta (band B3), under the per-diem table in force since 2026-01-01:
- Lodging cap: **139 USD per night**
- Receipt threshold: **45 USD** — above this amount, a receipt must be kept (this is the per-diem-specific threshold, not the general domestic KRW evidence rule).

(For context, the same row also lists meals at 81 USD/day and incidentals at 16 USD/day, though these weren't asked for.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions applies to today's date)
- /v1/nodes/hard-perdiem-legend-grade/body (junior analyst → G1)
- /v1/nodes/hard-perdiem-legend-band/body (Jakarta → B3)
- /v1/nodes/hard-perdiem-legend-stay/body (three weeks → S4)
- /v1/nodes/hard-perdiem-row-grade-g1-band-b3-stay-s4/body (the answer: lodging cap and receipt threshold)

4. **Notes**
- Overseas per-diem has three superseded/current versions living side by side (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and the oldest one gives no indication it's been replaced. The legend-revision doc is the only thing that tells you which applies to today's date (2026-09-20 → current table, `sec-hard-perdiem`). Easy to grab the wrong version if you don't stop for that check.
- The per-diem row has its own field literally labeled "Receipt threshold," which directly answers "above what amount do I have to keep the receipt." I almost treated the general evidence/qualifying-evidence rule (30,000 KRW threshold for needing a tax-traceable document, from /v1/nodes/evidence/body) as the answer instead — but that's a domestic, KRW-denominated rule about what kind of document qualifies as evidence, a different question from the overseas per-diem's own USD receipt threshold. Worth flagging because both are plausible "receipt threshold" answers and they're in different currencies for different purposes.
- The three qualifiers (grade, band, stay) each required a separate legend lookup — none of the values are guessable, and the per-diem row itself explicitly says the legends are the only place the mapping is written down.
