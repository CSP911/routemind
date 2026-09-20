1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s4/body

2. **Answer**: Lodging cap is 235 USD per night. Above 35 USD (the receipt threshold), a receipt must be kept.

3. **Source**: /v1/nodes/hard-perdiem-row-grade-g3-band-b1-stay-s4/body

4. **Notes**: The expense region table flagged up front that overseas per-diem has THREE historical versions (`overseas-rates`, `hard-perdiem-v2`, and the current `sec-hard-perdiem`), which is an easy place to grab a superseded rate by mistake — the row's own footer confirms `sec-hard-perdiem` is the one in force from 2026-01-01, which covers today's date. Since the question already gave grade, band, and stay codes directly (G3, B1, S4), I didn't need to open the grade/band/stay legend files to translate a job title, destination city, or trip length into a code — going straight to the row address was correct and saved a few hops. No ambiguity in the final row itself: it names both "Lodging, per night" and "Receipt threshold" explicitly, so the two answers map cleanly onto the two halves of the question.
