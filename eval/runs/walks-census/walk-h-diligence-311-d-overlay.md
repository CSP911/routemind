1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O4, value W2, goods K2: is a site visit required, and what is the re-review frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, likely holds origin/value/goods matrix with site visit and review frequency columns" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table; need to confirm which is current for today's date 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_2d69b5 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body
```

2. **Answer**
No, a site visit is not required. The file (re-review) is looked at again every 24 months.
(For reference, screening score required is 83 and financial statements must be from the last year — not asked, but part of the same row.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirms the current table, in force 2026-01-01 onward, applies to today's date 2026-09-20)
- /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k2/body (the row with the actual figures)

4. **Notes**
The procurement area table warned upfront that supplier due diligence has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), each at a different address, and that the oldest version says nothing about being superseded — so trusting it blindly would be wrong for a current-dated question. Checked the legend-revision page before trusting the current table (`sec-hard-diligence`) to make sure 2026-09-20 actually falls in its range; it does, so no correction was needed here, but skipping that check would have been an easy way to get the right answer for the wrong reason (or the wrong answer, on a differently-dated question).

The row address for O4/W2/K2 was printed directly under the /v1/nodes/sec-hard-diligence table heading when the overlay was created (that table lists all 4×4×4 = 64 rows, one per origin/value/goods combination), so it was never explicitly added to the overlay with `overlay add` — it was read straight from the printed list. The overlay tool flagged this as "reached" (answered from somewhere not explicitly named as a member) when closed, which is just a bookkeeping note, not an error.
