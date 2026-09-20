---
id: prepaid-card-issuance-approval-table
name: "Prepaid card issuance by amount"
kind: table
one_liner: "The approver a prepaid card request needs, banded by the amount it's loaded with"
parent: sec-prepaid-and-virtual-cards
---
# Prepaid card issuance by amount

The amount a prepaid card is issued for decides who has to approve it, following the same logic as any other expense request rather than a scale built specifically for prepaid cards.

## Approval bands

| Amount loaded | Approver |
|---|---|
| Up to 500,000 KRW | Team lead |
| 500,000–3,000,000 KRW | Division head |
| Above 3,000,000 KRW | Division head and above, per the standard expense approval chain |

## The trap
**Splitting one project's card into two issuance requests to stay under the team lead's ceiling gets flagged the same way a split payment does on a receipt.** Finance checks issuance requests against the project name and date range, not just the amount on each form, and treats two requests for one purpose as a single spend for approval purposes.

## After issuance
The approval band only governs the initial load. A later top-up that pushes the cumulative total into a higher band needs that band's approver, even if the top-up amount alone would have cleared the lower one.
