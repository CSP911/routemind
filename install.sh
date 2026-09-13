#!/bin/sh
# Bring this up on a machine that has never run it.
#
#   ./install.sh                        ask about the LLM if there is a terminal to ask in
#   ./install.sh --no-llm               do not ask; run without one
#   ./install.sh --llm-provider openai|anthropic|litellm --llm-url URL --llm-key KEY --llm-model MODEL
#   KNOWLEDGE_LLM_PROVIDER=... KNOWLEDGE_LLM_URL=... KNOWLEDGE_LLM_KEY=... KNOWLEDGE_LLM_MODEL=... ./install.sh
#
# Safe to run again: an existing .env is kept, and only the settings you pass are replaced.
#
# The LLM is optional. Every routing line is written by a person either way; with an LLM, a Suggest
# button beside each one drafts it, and without one that button is shown disabled — the screen is the
# same, so nothing is hidden and nothing breaks. It is asked about here because the button saying
# "no LLM is configured" is the only other place a person would find out.
set -e
cd "$(dirname "$0")"

LLM_URL="${KNOWLEDGE_LLM_URL:-}"; LLM_KEY="${KNOWLEDGE_LLM_KEY:-}"; LLM_MODEL="${KNOWLEDGE_LLM_MODEL:-}"
LLM_PROVIDER="${KNOWLEDGE_LLM_PROVIDER:-}"
DEFAULT_BASE_openai=https://api.openai.com
DEFAULT_BASE_anthropic=https://api.anthropic.com
ASK=1
while [ $# -gt 0 ]; do
  case "$1" in
    --no-llm)     ASK=0 ;;
    --llm-url)    LLM_URL="$2"; ASK=0; shift ;;
    --llm-key)    LLM_KEY="$2"; ASK=0; shift ;;
    --llm-model)    LLM_MODEL="$2"; ASK=0; shift ;;
    --llm-provider) LLM_PROVIDER="$2"; ASK=0; shift ;;
    -h|--help)    sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) printf 'unknown option: %s (try --help)\n' "$1" >&2; exit 2 ;;
  esac
  shift
done
[ -n "$LLM_URL" ] && ASK=0

[ -f .env ] || cp .env.example .env
grep -q '^KNOWLEDGE_UID=' .env || printf 'KNOWLEDGE_UID=%s\nKNOWLEDGE_GID=%s\n' "$(id -u)" "$(id -g)" >> .env

# Only when there is a terminal AND the .env has no answer yet. A re-run, or a scripted one, must not
# stop and wait for somebody who is not there.
if [ "$ASK" = 1 ] && [ -t 0 ] && ! grep -q '^ONTOLOGY_LLM_BASE_URL=.\+' .env; then
  cat <<'TXT'

An LLM is optional. Everything works without one.

You write every routing line yourself — when to choose an area, what a node
holds, what a document is for — and each field shows how to write it. With an
LLM, a "Suggest" button beside each field drafts the line for you to edit;
without one, that button is shown disabled.

openai, anthropic, or a LiteLLM-style gateway. Press Enter to skip; you can
add it later by editing .env and running this again.

TXT
  printf 'Provider — openai, anthropic, litellm (Enter to skip): '; read -r LLM_PROVIDER
  if [ -n "$LLM_PROVIDER" ]; then
    # The two hosted providers have one address each; a gateway is wherever you put it.
    case "$LLM_PROVIDER" in
      openai)    SUGGEST="$DEFAULT_BASE_openai" ;;
      anthropic) SUGGEST="$DEFAULT_BASE_anthropic" ;;
      *)         SUGGEST="" ;;
    esac
    printf 'Base URL, no /v1 %s: ' "${SUGGEST:+[$SUGGEST]}"; read -r LLM_URL
    [ -z "$LLM_URL" ] && LLM_URL="$SUGGEST"
    printf 'API key: '; read -r LLM_KEY
    # Which models this key can use is a question only the provider can answer, and the answer
    # changes. Asking it beats any list written into this repository, which would start going stale
    # the day it was written and would fail by refusing a model that exists.
    if [ -n "$LLM_URL" ] && [ -n "$LLM_KEY" ] && command -v python3 >/dev/null 2>&1; then
      printf '\nasking %s which models this key can use...\n' "$LLM_PROVIDER"
      ./check/llm-probe.py --provider "$LLM_PROVIDER" --base "$LLM_URL" --key "$LLM_KEY" 2>&1 | head -40 || true
      printf '\n'
    fi
    printf 'Model: '; read -r LLM_MODEL
  fi
fi
[ -n "$LLM_URL" ] && [ -z "$LLM_PROVIDER" ] && LLM_PROVIDER=litellm

# Replace a key in .env rather than appending a second copy of it — compose reads the last one, so an
# appended override works by accident and a corrected value silently does not.
setenv() {
  k="$1"; v="$2"
  if grep -q "^$k=" .env; then
    tmp="$(mktemp)"; grep -v "^$k=" .env > "$tmp"; printf '%s=%s\n' "$k" "$v" >> "$tmp"; mv "$tmp" .env
  else printf '%s=%s\n' "$k" "$v" >> .env; fi
}
if [ -n "$LLM_URL" ]; then
  setenv ONTOLOGY_LLM_PROVIDER "$LLM_PROVIDER"
  setenv ONTOLOGY_LLM_BASE_URL "$LLM_URL"
  setenv ONTOLOGY_LLM_API_KEY  "$LLM_KEY"
  setenv ONTOLOGY_LLM_MODEL    "$LLM_MODEL"
fi

# Before compose, not after: a bind-mount source Docker has to invent is invented as root, and this
# container runs as you so that it can commit into your repository.
mkdir -p data/repo data/publish data/overlays data/harness data/exchange data/access

# The link this install already has: one backbone, meeting at its own exchange.
#
# **Wired now rather than when a second backbone arrives.** Both halves of a link are declarations —
# the backbone names the exchange, the exchange names the backbone — and writing them at install time
# means adding a second backbone touches nothing that already works. Doing it later would mean
# rewriting the first backbone's peers.yaml at exactly the moment somebody is busy adding a second.
#
# The secret is generated once and kept. It is the same one in both directions, which is what lets the
# exchange tell who is calling.
if ! grep -q '^EXCHANGE_TOKEN_HOME=.\+' .env; then
  setenv EXCHANGE_TOKEN_HOME "$(head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')"
fi
# An install made before 2026-09-13 has a peers.yaml naming the exchange with no `kind:` on it, and
# that entry is skipped by the block below because the file exists. Said rather than edited: this is
# somebody's repository, a write here makes the tree dirty and every later write is then refused
# until they commit something they did not do. The screen says the same thing on its own.
if [ -f data/repo/peers.yaml ] && grep -q 'url: *http://exchange:8110' data/repo/peers.yaml \
   && ! grep -q 'kind: *exchange' data/repo/peers.yaml; then
  printf "  ! data/repo/peers.yaml names the exchange without 'kind: exchange'.\n"
  printf "    Add that line and commit it. Without it this backbone filters for the room instead\n"
  printf "    of for its members, so an area's audience and a line written for one peer do\n"
  printf "    nothing — and nothing anywhere looks broken. The map's bar says the same.\n"
fi
if [ ! -f data/repo/peers.yaml ]; then
  cat > data/repo/peers.yaml <<'YAML'
# Who this backbone is linked to. The token for each is in the environment, not here — this file is
# versioned and reviewed like the rest of what this backbone is, and a secret is neither.
peers:
  - name: ix
    label: EXCHANGE
    url: http://exchange:8110
    # A room, not a backbone. It changes one thing: this backbone believes it when it says which of
    # its members a document is being fetched for, which is what makes an area's audience mean
    # anything behind an exchange. An ordinary peer saying the same is not believed.
    kind: exchange
    token_env: ONTOLOGY_PEER_TOKEN_IX
YAML
fi
if [ ! -f data/exchange/members.yaml ]; then
  cat > data/exchange/members.yaml <<'YAML'
# Who meets here. The token for each is in the environment, not in this file.
#
# This is the exchange's half of the declaration; each backbone names the exchange in its own
# peers.yaml. Both halves are needed, so nobody is enrolled by one side alone.
members:
  - name: home
    label: HOME
    url: http://ontology:8100
    token_env: EXCHANGE_TOKEN_HOME
YAML
fi

docker compose up -d --build

# One base URL, used to wait and then to check. Computing it twice is how the check ends up talking
# to a different install than the one just started — which it did, and passed.
# The **last** match, which is the one docker compose uses, and trimmed. Appending a line to .env
# rather than editing the one already there is an ordinary thing to do; with `head`-style behaviour
# the installer waited on one port while the container published another, and the message was that
# nothing came up. Two readers of one file have to agree about which value wins.
PORT="$(grep -E '^[[:space:]]*WEB_PORT=' .env | tail -n 1 | cut -d= -f2- | tr -d '"'"'"' \r' | tr -d '[:space:]')"
BASE="http://127.0.0.1:${PORT:-8080}"
printf 'waiting for %s' "$BASE"
i=0
while [ $i -lt 60 ]; do
  if curl -fsS -o /dev/null "$BASE/api/app-config" 2>/dev/null; then
    printf '\n\n'
    # What this install can actually do, from the install itself rather than from what was typed —
    # a key that is wrong, or a URL with /v1 on the end, answers here and not in a support thread.
    cfg=$(curl -fsS "$BASE/api/app-config" 2>/dev/null || echo '{}')
    derives=$(printf '%s' "$cfg" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("derives"))' 2>/dev/null || echo unknown)
    prov=$(printf '%s' "$cfg" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("llm_provider") or "")' 2>/dev/null || echo "")
    known=$(printf '%s' "$cfg" | python3 -c 'import json,sys; print(" ".join(json.load(sys.stdin).get("llm_providers") or []))' 2>/dev/null || echo "")
    if [ "$derives" = "True" ]; then
      printf 'RouteMind is at %s — with %s: it derives addresses and drafts conditions.\n\n' "$BASE" "$prov"
    else
      printf 'RouteMind is at %s — without an LLM: you type the address and the condition yourself.\n' "$BASE"
      # A provider this build does not know turns the LLM off, and "off" alone reads as a forgotten
      # key. Say which it is, because the fix is different.
      want=$(grep -E '^ONTOLOGY_LLM_PROVIDER=' .env | cut -d= -f2)
      if [ -n "$want" ] && [ -n "$known" ] && ! printf '%s' " $known " | grep -q " $want "; then
        printf 'ONTOLOGY_LLM_PROVIDER=%s is not one this build knows (%s).\n' "$want" "$known"
      else
        printf 'To add one: set ONTOLOGY_LLM_* in .env and run ./install.sh again.\n'
      fi
      printf '\n'
    fi
    exec ./check/smoke.sh "$BASE"
  fi
  printf '.'; sleep 2; i=$((i+1))
done
printf '\nit did not come up. docker compose logs\n' >&2
exit 1
