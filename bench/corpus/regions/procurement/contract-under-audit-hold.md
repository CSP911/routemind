---
id: contract-under-audit-hold
name: "Contracts held for audit"
kind: rule
one_liner: "What changes in custody once an original is pulled for internal or external audit"
parent: sec-contract-custody-cases
---
# Contracts held for audit

Pulling an original for audit puts a hold flag on its custody log entry. While flagged, the original cannot be borrowed for any other purpose, including a legitimate business need like a renewal negotiation.

| Trigger | Effect |
|---|---|
| Internal audit request | Hold flag set; department notified by GA |
| External or regulatory audit | Hold flag set; retention clock suspended until audit closes |

The normal 5-year retention window does not run down while a hold is active. It resumes only once the auditor releases the file.

## The trap

**People assume an audit hold only affects the copy the finance team is working from.** It doesn't — the flag sits on the custody log entry itself, so it blocks every subsequent request against that original, not just the one the audit is looking at.

If the original can't be located at all when a hold is requested, that's a separate problem with its own escalation path.
