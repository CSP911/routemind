1. **Commands**:
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 5 years tenure, fully remote (from home): monthly leave accrual rate and max carryover/holding into January?" --member /v1/regions/attendance "leave accrual, carryover rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body
./bench/rmcli.py overlay add --id ov_2026-09-20_44c494 --address /v1/nodes/hard-accrual-legend-type/body --why "maps 'here from our partner firm' to type E4"
./bench/rmcli.py overlay add --id ov_2026-09-20_44c494 --address /v1/nodes/hard-accrual-legend-tenure/body --why "maps 'been here five years' to tenure T3"
./bench/rmcli.py overlay add --id ov_2026-09-20_44c494 --address /v1/nodes/hard-accrual-legend-site/body --why "maps 'fully from home' to site L4"
./bench/rmcli.py overlay add --id ov_2026-09-20_44c494 --address /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body --why "exact row for E4/T3/L4: 1.58 days/month accrual, 13-day carry-over limit"
./bench/rmcli.py overlay close --id ov_2026-09-20_44c494 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body
```

2. **Answer**: 1.58 days accrue per month. The carry-over limit (the most you can be holding going into January) is 13 days. Notice required to take leave is 5 working days, and leave does not accrue during unpaid leave. This is the row for type E4 (partner-firm staff), tenure T3 (five years), site L4 (fully from home), from the current accrual table in force since 2026-01-01. An excess above 13 days that wasn't pre-approved is settled at 13 and the rest is not recoverable; an unavoidable excess needs a written statement and is decided by the budget holder.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual-table versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-accrual-legend-type/body (mapped "here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "been here five years" → tenure T3)
- /v1/nodes/hard-accrual-legend-site/body (mapped "fully from home" → site L4)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l4/body (the answer: 1.58 days/month accrual, 13-day carry-over limit)

4. **Notes**: The main trap here is the three-version accrual history — `sec-hard-accrual` (current, since 2026-01-01), `hard-accrual-v2` (2024-07-01 to 2025-12-31), and the oldest `leave-accrual`, which the legend page explicitly warns "says nothing at all about having been replaced." Since today is 2026-09-20, the current table is right, but it would have been easy to grab the wrong one if I hadn't checked the revision-legend page first, especially since the oldest version gives no hint that newer ones exist. All three qualifiers in the question (partner firm, five years, fully from home) happened to map to exact rows in their respective legends — no nearest-match judgment calls were needed, which is not something I could assume going in.
