---
id: policy-version-history
name: "Tracking a policy's versions"
kind: table
one_liner: "a policy amended more than once carries a separate retention clock for each version, not one for the subject"
parent: sec-policy-and-its-own-lifecycle
---
# Tracking a policy's versions

A policy that has been amended more than once needs its history kept straight, because retention and withdrawal rules apply to each version, not to the subject as a whole.

## What the version record holds

| Field | Purpose |
|---|---|
| Version date | When this version was published |
| Supersedes | The version it replaces, named explicitly |
| Withdrawn date | Left blank until the version is retired |
| Retention | 5 years as a drafts-and-proposals record, from the date of that version's own filing |

## The trap

**Retention runs per version, not per policy.** A policy amended three times has three proposal records, each with its own five-year clock starting from its own filing date — destroying the earliest version early because "the policy is still current" removes the only record of what the rule said before the most recent change, which is exactly what an audit asks for.

Keeping the chain of versions intact is what makes a withdrawal or a conflict easy to resolve later rather than a guess.
