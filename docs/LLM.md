# With an LLM

Optional, and it changes exactly one thing: a **✨ Suggest** button beside each routing line drafts it
for you to edit. Leave it out and those buttons are shown disabled — everything else is identical,
because you write every line either way.

**First, ask the provider what the key can actually use:**

```sh
./check/llm-probe.py --provider openai --base https://api.openai.com --key $KEY
./check/llm-probe.py --provider openai --base https://api.openai.com --key $KEY --model gpt-4o-mini
```

It lists the models the key can see, then makes one small call with the one you pick. No model list is
written into this repository — one would start going stale the day it was written, and would reject
new models rather than accept them.

**Then install with it.** Three providers, and they are genuinely different wires rather than one with
options — the path, the auth header, where the system prompt goes and the shape of the reply all differ:

```sh
# OpenAI
./install.sh --llm-provider openai \
             --llm-url https://api.openai.com --llm-key sk-... --llm-model gpt-4o-mini

# Anthropic
./install.sh --llm-provider anthropic \
             --llm-url https://api.anthropic.com --llm-key sk-ant-... --llm-model claude-sonnet-5

# A LiteLLM-style gateway, or anything OpenAI-shaped — the default
./install.sh --llm-provider litellm \
             --llm-url https://your-gateway --llm-key ... --llm-model ...
```

Environment variables do the same, for CI:

```sh
KNOWLEDGE_LLM_PROVIDER=openai KNOWLEDGE_LLM_URL=https://api.openai.com \
KNOWLEDGE_LLM_KEY=sk-... KNOWLEDGE_LLM_MODEL=gpt-4o-mini ./install.sh
```

Two rules account for most misconfigurations:

- **Give the base URL without `/v1`.** The client appends the rest itself.
- **A provider this build does not know turns the LLM off** and says so, in the startup log and in what
  `install.sh` prints, rather than being quietly ignored.

Because `install.sh` finishes by reading `/api/app-config`, a wrong key or a trailing `/v1` shows up
there and not later:

```
RouteMind is at http://127.0.0.1:8080 — with openai: it derives addresses and drafts conditions.
RouteMind is at http://127.0.0.1:8080 — without an LLM: you type the address and the condition yourself.
```

To add or change one afterwards, run `./install.sh` again with the flags, or edit the `ONTOLOGY_LLM_*`
lines in `.env` and re-run it.

## What it does and does not do

**You write every routing line yourself**, with a model or without: when an agent should choose an
area, what a node holds, what a document is for. Each field shows how to write it, and **Suggest fills
the box — it does not save.** Nothing is written until you press the form's own button. The address a
name gives is filled in as you type the name, and you can change it before saving. The one thing only
a model can do is give an address to a name that is not in Latin letters; without one, you type that
address.

**A kind is never asked for.** Nothing reads one until you declare `edge_rules`, so RouteMind picks it
with an LLM where there is one and takes `default_kind` from `vocab.yaml` where there is not. The
response says `kind_generated` either way, so a domain that later makes kinds mean something can find
the ones nobody actually chose.

`ONTOLOGY_LLM_MAX_TOKENS` and `ONTOLOGY_LLM_TEMPERATURE` are yours. **`response_format` is not**: the
code sets it per call — the two prompts whose answer is parsed as JSON ask for JSON, the four that read
one line do not. Setting it by hand breaks the parsing, and the only symptom is that the model seems to
be answering strangely.

`./check/llm-paths.sh` runs both modes, so a change to one does not quietly break the other.

---

Back to [the README](../README.md).
