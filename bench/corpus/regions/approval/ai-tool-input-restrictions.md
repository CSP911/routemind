---
id: ai-tool-input-restrictions
name: "What can't be pasted into an AI tool"
kind: rule
one_liner: "Personal data, unsigned contract terms, and unpublished figures stay out regardless of which tool is asking"
parent: sec-use-of-ai-tools
---
# What can't be pasted into an AI tool

Some material cannot go into any AI tool, including an approved one, unless the specific use has been cleared with Legal in advance.

| Restricted input | Why |
|---|---|
| Personal data (names, contact details, employment records) | Collection and use are already scoped to a stated purpose; a tool query is a new purpose |
| Draft contract terms before signing | Commercial terms are not yet final and may not be disclosable |
| Unpublished financial figures | Same disclosure risk as sharing them outside the company |
| Source code or documents under an NDA | The NDA binds the company, not the tool's vendor |

**Summarizing a document is still pasting it in.** The model receives the same text whether the request is "copy this" or "summarize this" — shortening the prompt does not shorten what the tool retains.

Where a use case needs one of these inputs, the request goes through the same approval as adding a new tool, not around it.
