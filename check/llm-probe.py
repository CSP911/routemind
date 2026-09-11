#!/usr/bin/env python3
"""Ask a provider what this key can actually use, and try one call.

    ./check/llm-probe.py --provider anthropic --base https://api.anthropic.com --key $KEY
    ./check/llm-probe.py --provider openai    --base https://api.openai.com    --key $KEY --model gpt-4o-mini

Two questions, in the order they matter:

  1. which models does this key list?   — better than any list written into this repository, which
                                          would start going stale the day it was written and would
                                          reject new models rather than accept them
  2. does one real call come back?      — a key that lists models can still fail on a call: a wrong
                                          base URL, a model the key is not entitled to, a parameter
                                          the provider rejects

Read-only. It lists and sends one tiny completion; it writes nothing.
"""
import argparse, json, sys, urllib.error, urllib.request

WIRE = {
    # path, auth header, and how the answer is shaped. anthropic is not OpenAI-shaped: the system
    # prompt is a top-level field and the reply is content[].text.
    "openai":    {"models": "/v1/models", "chat": "/v1/chat/completions"},
    "litellm":   {"models": "/v1/models", "chat": "/v1/chat/completions"},
    "anthropic": {"models": "/v1/models", "chat": "/v1/messages"},
}


def headers(provider, key):
    if provider == "anthropic":
        return {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    return {"Authorization": "Bearer " + key, "Content-Type": "application/json"}


def call(url, hdrs, payload=None, timeout=60):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=hdrs, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--provider", required=True, choices=sorted(WIRE))
    p.add_argument("--base", required=True, help="base URL WITHOUT /v1")
    p.add_argument("--key", required=True)
    p.add_argument("--model", help="if given, one real call is made with it")
    p.add_argument("--max-tokens", type=int, default=64)
    p.add_argument("--temperature", type=float, default=0.0)
    a = p.parse_args()
    base, w = a.base.rstrip("/"), WIRE[a.provider]
    hdrs = headers(a.provider, a.key)

    try:
        listed = call(base + w["models"], hdrs)
    except urllib.error.HTTPError as e:
        print(f"FAIL listing models: HTTP {e.code} {e.read().decode('utf-8','replace')[:200]}")
        return 1
    except Exception as e:
        print(f"FAIL listing models: {type(e).__name__}: {e}")
        return 1
    ids = sorted(m.get("id", "") for m in (listed.get("data") or []))
    print(f"ok   {len(ids)} models this key can list")
    for i in ids: print("      " + i)

    if not a.model:
        print("\n(no --model given; skipping the call. Pick one above.)")
        return 0
    if a.model not in ids:
        print(f"\nnote  {a.model} is not in that list — trying it anyway, since a list can lag entitlements")

    if a.provider == "anthropic":
        payload = {"model": a.model, "system": "Reply with exactly: ok",
                   "messages": [{"role": "user", "content": "say ok"}],
                   "max_tokens": a.max_tokens, "temperature": a.temperature}
    else:
        payload = {"model": a.model,
                   "messages": [{"role": "system", "content": "Reply with exactly: ok"},
                                {"role": "user", "content": "say ok"}],
                   "max_tokens": a.max_tokens, "temperature": a.temperature}
    try:
        out = call(base + w["chat"], hdrs, payload)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        print(f"\nFAIL one call: HTTP {e.code} {body}")
        # The two rejections worth naming, because both look like "the model is broken" otherwise.
        if "max_completion_tokens" in body: print("      → this model wants max_completion_tokens, not max_tokens")
        if "temperature" in body: print("      → this model does not accept the temperature you set")
        return 1
    text = (out["content"][0]["text"] if a.provider == "anthropic"
            else out["choices"][0]["message"]["content"])
    print(f"\nok   one call came back: {text.strip()[:80]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
