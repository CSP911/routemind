1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body
```

2. **Answer**
For category C3, amount V2, term M2 (in force from 2026-01-01, current as of 2026-09-20/21):
- Delegation limit: 5,037 thousand KRW
- Signs it off: the department head
- Competing quotes required: two — so yes, two competing quotes (other prices) have to be obtained first
- Working days to expect: 6

3. **Source**
- `/v1/nodes/hard-threshold-legend-revision/body` — confirmed which of the three approval-threshold versions applies to today's date (the current one, since 2026-01-01)
- `/v1/nodes/sec-hard-threshold` — table listing, located the exact row address for category C3, amount V2, term M2
- `/v1/nodes/hard-threshold-row-category-c3-amount-v2-term-m2/body` — the answer itself (signer and quote requirement)

4. **Notes**
- The approval-threshold subject has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) living side by side with no marker on the oldest saying it was replaced. The legend-revision page is the only thing that makes date-based selection safe, and it explicitly warns that reaching for the newest table is wrong for anything before 2026-01-01. Today's date (2026-09-20/21) falls under the current table, so that risk didn't bite here, but skipping that check would have been the easy mistake.
- The question already gave the row qualifiers as raw codes (C3, V2, M2), so the category legend read was really just a sanity check — not needed to derive the code from a plain-language description the way it would be for a question phrased as "flights and hotels." No amount or term legend was read since those codes were likewise given directly and the row address could be built from them without ambiguity.
- The row's "competing quotes: two" line directly answers "do I have to get other prices first" — it wasn't in a separate document, so no extra hop was needed once the row was open.
