1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
```

2. **Answer**
Under the version in force in October 2024 (`hard-diligence-v2`, in effect 2024-07-01 to 2025-12-31), the origin O2 / value W2 cell of the checks-required matrix reads **35**. The document gives this only as a raw numeric code in the origin-by-value table — there is no legend in this version decoding "35" into a named screening procedure (unlike the current, post-2026-01-01 table, which has separate legend pages for origin/value/goods codes). So the figure is 35; what it means in plain-English screening terms is not stated anywhere I could find.

3. **Source**
- `/v1/nodes/hard-diligence-legend-revision/body` (established which version covers Oct 2024)
- `/v1/nodes/hard-diligence-v2/body` (the actual O2×W2 = 35 figure)

4. **Notes**
- There are three versions of supplier due diligence with overlapping-looking scope, and the legend page is explicit that reaching for the current (2026-01-01+) table would be wrong here — October 2024 falls in the *middle* version (`hard-diligence-v2`), not the oldest and not the current one. Easy to get wrong if you jump straight to `sec-hard-diligence` because it's labeled "THE CURRENT... TABLE" and looks most complete.
- The v2 table's own text is internally confusing: the matrix is headed "The checks required, by origin and value," but the sentence right below it says "the checks required ... followed the supplier due diligence rule unchanged" beyond that column — i.e., it uses the phrase "checks required" both for the varying matrix value and for the fixed three-check base rule (sanctions/ownership, code of conduct, disqualification screen) from the pre-2024-07-01 document. I could not find anywhere that decodes what the number 35 itself represents (a day count? a check tier? something else) — it's presented as a bare figure with no legend, unlike the current table's three explicit legend files (origin/value/goods). I'm reporting the figure as found (35) rather than guessing at its meaning.
- I did not open the per-combination row files under `sec-hard-diligence` (e.g. `hard-diligence-row-origin-o2-value-w2-goods-k*`) because those belong to the 2026-01-01+ version, which is out of scope for an October 2024 question, and mixing them in would misattribute a post-2026 rule to 2024.
