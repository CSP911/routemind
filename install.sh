#!/bin/sh
# Bring this up on a machine that has never run it.
#
#   ./install.sh                        ask which port, and about the LLM
#   ./install.sh --port 9000
#   ./install.sh --no-llm               do not ask about the LLM; run without one
#   ./install.sh --example              start from the example back office (asked on a first install)
#   ./install.sh --no-example           start from an empty map, without asking
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
EXAMPLE=""
PORT="${WEB_PORT:-}"
while [ $# -gt 0 ]; do
  case "$1" in
    # Named the exchange this install met other backbones at; there is no exchange since 2026-10-08.
    # Still accepted, so a command copied from an older page does not stop at an unknown option.
    --name)       printf '  --name is no longer used (there is no exchange to name) — ignored\n'; shift ;;
    --port)       PORT="${2:-}"; [ -n "$PORT" ] || { printf '  ! --port takes a number\n' >&2; exit 2; }; shift ;;
    --no-llm)     ASK=0 ;;
    --example)    EXAMPLE=yes ;;
    --no-example) EXAMPLE=no ;;
    --llm-url)    LLM_URL="$2"; ASK=0; shift ;;
    --llm-key)    LLM_KEY="$2"; ASK=0; shift ;;
    --llm-model)    LLM_MODEL="$2"; ASK=0; shift ;;
    --llm-provider) LLM_PROVIDER="$2"; ASK=0; shift ;;
    -h|--help)    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) printf 'unknown option: %s (try --help)\n' "$1" >&2; exit 2 ;;
  esac
  shift
done
[ -n "$LLM_URL" ] && ASK=0

NEW_ENV=""
[ -f .env ] || { cp .env.example .env; NEW_ENV=1; }
# A first run refused before anything started (a bad or busy port, a name another checkout holds) takes
# back the .env it just made. Left behind, the next run read it as an existing install's: it skipped
# the port question and the path-suffixed name (operator QA, 2026-10-10).
refuse() { [ -n "$NEW_ENV" ] && rm -f .env; exit 2; }
grep -q '^KNOWLEDGE_UID=' .env || printf 'KNOWLEDGE_UID=%s\nKNOWLEDGE_GID=%s\n' "$(id -u)" "$(id -g)" >> .env

# Replace a key in .env rather than appending a second copy of it — compose reads the last one, so an
# appended override works by accident and a corrected value silently does not.
setenv() {
  k="$1"; v="$2"
  if grep -q "^$k=" .env; then
    tmp="$(mktemp)"; grep -v "^$k=" .env > "$tmp"; printf '%s=%s\n' "$k" "$v" >> "$tmp"; mv "$tmp" .env
  else printf '%s=%s\n' "$k" "$v" >> .env; fi
}

# ── where to answer ───────────────────────────────────────────────────────────
# Asked only where there is a terminal and the answer is not already in .env, the same rule the LLM
# question follows: a re-run or a scripted install must not stop and wait for somebody who is not
# there. It has a working default, so pressing Enter is a complete answer.
# A new .env already holds WEB_PORT=8080 from .env.example, so "not in .env" was never true and the
# question was never asked (QA, 2026-10-10). A new .env is the first install, and that is when to ask.
if [ -z "$PORT" ] && [ -t 0 ] && { [ -n "$NEW_ENV" ] || ! grep -q '^WEB_PORT=.\+' .env; }; then
  printf '\nWhich port should the map answer on?\n  [8080] > '
  read -r PORT || PORT=""
fi
if [ -n "$PORT" ]; then
  case "$PORT" in
    ''|*[!0-9]*) printf '  ! --port takes a number\n' >&2; refuse ;;
    # 99999 was written to .env as it was, and from then on even `docker compose ps` failed on it.
    *) [ "$PORT" -ge 1 ] && [ "$PORT" -le 65535 ] || { printf '  ! a port is 1 to 65535, not %s\n' "$PORT" >&2; refuse; }
       setenv WEB_PORT "$PORT" ;;
  esac
fi

# `.mcp.json` names no port: the MCP server reads WEB_PORT from this .env itself (mcp/knowledge_mcp.py).
# It used to be rewritten here, which left every checkout on another port with a modified tracked file,
# a `git pull` that could refuse, and a port changed by hand in .env pointing Claude Code at the old one.

# Each checkout builds its own images. The tag was shared, so a second install on the same machine
# retagged the first one's images, and the first picked up the second's code at its next recreate.
#
# The directory name alone was not enough: compose names the *containers* after it too, so a second
# clone called `routemind` somewhere else recreated the first one's containers from its own code and
# the first install went dark without a word (QA, 2026-10-10). A new install takes the name plus a few
# digits of its path, for the images and the containers both. An existing one keeps what it has —
# renaming its project would orphan the containers it is running.
SLUG="$(basename "$PWD" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9.\n-' '-' | cut -c1-32)"
if [ -n "$NEW_ENV" ]; then
  PATHSUM="$(printf '%s' "$(pwd -P)" | cksum | cut -d' ' -f1 | cut -c1-6)"
  setenv COMPOSE_PROJECT_NAME "$SLUG-$PATHSUM"
  setenv IMAGE_TAG "$SLUG-$PATHSUM"
fi
grep -q '^IMAGE_TAG=.\+' .env || setenv IMAGE_TAG "$SLUG"

# Whatever the name, never take over containers another checkout started.
PROJECT="$(docker compose config 2>/dev/null | sed -n 's/^name: //p' | head -1)"
if [ -n "$PROJECT" ]; then
  OTHER="$(docker ps -a --filter "label=com.docker.compose.project=$PROJECT" --format '{{.Label "com.docker.compose.project.working_dir"}}' 2>/dev/null | sort -u | grep -vxF "$PWD" | grep -vxF "$(pwd -P)" | head -1)"
  if [ -n "$OTHER" ]; then
    printf '\n  ! another RouteMind is running under the name "%s", from\n      %s\n' "$PROJECT" "$OTHER" >&2
    printf '    Starting here would replace its containers with this checkout'"'"'s. Give this one its own name:\n' >&2
    printf '      echo COMPOSE_PROJECT_NAME=%s-2 >> .env && echo IMAGE_TAG=%s-2 >> .env && ./install.sh\n' "$PROJECT" "$PROJECT" >&2
    refuse
  fi
fi

# A port something else holds used to surface after the build, as Docker's own message, with half the
# install started. Asked first, and the one exception is our own web container already on it.
WANT="$(grep -E '^[[:space:]]*WEB_PORT=' .env | tail -n 1 | cut -d= -f2- | tr -d '"'"'"' \r' | tr -d '[:space:]')"
WANT="${WANT:-8080}"
if command -v python3 >/dev/null 2>&1 && python3 -c "import socket,sys; s=socket.socket(); s.settimeout(0.5); sys.exit(0 if s.connect_ex(('127.0.0.1', $WANT)) == 0 else 1)" 2>/dev/null; then
  if ! docker ps --filter "label=com.docker.compose.project=$PROJECT" --filter "publish=$WANT" --format '{{.ID}}' 2>/dev/null | grep -q .; then
    FREE="$(python3 -c "import socket
for p in range($WANT + 1, min($WANT + 200, 65536)):
    s = socket.socket(); s.settimeout(0.2)
    if s.connect_ex(('127.0.0.1', p)) != 0: print(p); break" 2>/dev/null)"
    printf '\n  ! port %s is already in use by something else. Pick another:\n      ./install.sh --port %s\n' "$WANT" "${FREE:-$((WANT + 1))}" >&2
    refuse
  fi
fi

# Only when there is a terminal AND the .env has no answer yet. A re-run, or a scripted one, must not
# stop and wait for somebody who is not there.
if [ "$ASK" = 1 ] && [ -t 0 ] && ! grep -q '^ONTOLOGY_LLM_BASE_URL=.\+' .env && ! grep -q '^# llm: skipped' .env; then
  cat <<'TXT'

An LLM is optional. Everything works without one.

You write every routing line yourself — when to choose an area, what a node
holds, what a document is for — and each field shows how to write it. With an
LLM, a "Suggest" button beside each field drafts the line for you to edit;
without one, that button is shown disabled.

openai, anthropic, or a LiteLLM-style gateway. Press Enter to skip; you can
add it later by editing .env and running this again.

TXT
  printf 'Provider — openai, anthropic, litellm (Enter to skip): '; read -r LLM_PROVIDER || LLM_PROVIDER=""
  # Skipping is an answer, and it is kept: an update run must not ask it again every time.
  [ -z "$LLM_PROVIDER" ] && printf '# llm: skipped at install — set the ONTOLOGY_LLM_* lines in this file and run ./install.sh to add one\n' >> .env
  if [ -n "$LLM_PROVIDER" ]; then
    # The two hosted providers have one address each; a gateway is wherever you put it.
    case "$LLM_PROVIDER" in
      openai)    SUGGEST="$DEFAULT_BASE_openai" ;;
      anthropic) SUGGEST="$DEFAULT_BASE_anthropic" ;;
      *)         SUGGEST="" ;;
    esac
    printf 'Base URL, no /v1 %s: ' "${SUGGEST:+[$SUGGEST]}"; read -r LLM_URL || LLM_URL=""
    [ -z "$LLM_URL" ] && LLM_URL="$SUGGEST"
    printf 'API key: '; read -r LLM_KEY || LLM_KEY=""
    # Which models this key can use is a question only the provider can answer, and the answer
    # changes. Asking it beats any list written into this repository, which would start going stale
    # the day it was written and would fail by refusing a model that exists.
    if [ -n "$LLM_URL" ] && [ -n "$LLM_KEY" ] && command -v python3 >/dev/null 2>&1; then
      printf '\nasking %s which models this key can use...\n' "$LLM_PROVIDER"
      ./check/llm-probe.py --provider "$LLM_PROVIDER" --base "$LLM_URL" --key "$LLM_KEY" 2>&1 | head -40 || true
      printf '\n'
    fi
    printf 'Model: '; read -r LLM_MODEL || LLM_MODEL=""
  fi
fi
[ -n "$LLM_URL" ] && [ -z "$LLM_PROVIDER" ] && LLM_PROVIDER=litellm

if [ -n "$LLM_URL" ]; then
  setenv ONTOLOGY_LLM_PROVIDER "$LLM_PROVIDER"
  setenv ONTOLOGY_LLM_BASE_URL "$LLM_URL"
  setenv ONTOLOGY_LLM_API_KEY  "$LLM_KEY"
  setenv ONTOLOGY_LLM_MODEL    "$LLM_MODEL"
fi

# Before compose, not after: a bind-mount source Docker has to invent is invented as root, and this
# container runs as you so that it can commit into your repository.
mkdir -p data/repo data/overlays data/walks data/harness data/access

# A first install — nothing in data/repo yet — may start from the example back office instead of an
# empty map. Before compose, because the first boot is what makes data/repo a git repository and
# commits what is there; copied in afterwards it was an uncommitted tree that refused every write.
if [ -z "$(ls -A data/repo 2>/dev/null)" ]; then
  if [ -z "$EXAMPLE" ] && [ -t 0 ]; then
    printf '\nStart from the example back office (five areas, 74 documents) instead of an empty map? [Y/n] '
    read -r ans || ans=""
    case "$ans" in [nN]*) EXAMPLE=no ;; *) EXAMPLE=yes ;; esac
  fi
  if [ "$EXAMPLE" = yes ]; then
    cp -R examples/back-office/. data/repo/
    printf '  data/repo starts from examples/back-office — yours to change or replace.\n'
  elif [ -z "$EXAMPLE" ]; then
    # No terminal to ask on, and no flag: an empty map, which used to happen without a word.
    printf '\n  No terminal to ask on, so the map starts empty. For the example back office instead:\n'
    printf '    ./install.sh --example      (now, before the first start)   or later: ./ontology/reset.sh --example --yes\n'
  fi
fi

# The key another backbone's circuit presents to read the areas set `export` here. Generated once and
# kept; nothing crosses until somebody sets `export` on an area, so having a key is not sharing
# anything. An install made before 2026-10-08 has it as EXCHANGE_TOKEN_HOME, which compose still reads,
# so it is carried over under the new name rather than replaced — whoever holds it keeps working.
if ! grep -q '^KNOWLEDGE_CIRCUIT_TOKEN=.\+' .env; then
  OLD="$(grep '^EXCHANGE_TOKEN_HOME=' .env 2>/dev/null | tail -1 | cut -d= -f2-)"
  setenv KNOWLEDGE_CIRCUIT_TOKEN "${OLD:-$(head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')}"
fi

# --remove-orphans: an install from before 2026-10-08 still has containers for services that no longer
# exist (the exchange), and compose would warn about them on every start.
docker compose up -d --build --remove-orphans

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
      printf 'RouteMind is at %s — with %s: the ✨ Suggest buttons draft each line for you to edit.\n\n' "$BASE" "$prov"
    else
      printf 'RouteMind is at %s — without an LLM: you write each line yourself, and the ✨ Suggest buttons stay off.\n' "$BASE"
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
    # The checks are for this install, not for reading: ninety lines of them ("kn-file has no rule, on
    # purpose") ended every install. Kept in a file; shown only when one fails.
    SMOKE_LOG="data/install-checks.log"
    if ./check/smoke.sh "$BASE" > "$SMOKE_LOG" 2>&1; then
      printf 'The install checks passed (full output: %s).\n\n' "$SMOKE_LOG"
    else
      cat "$SMOKE_LOG"
      printf '\nThe install is up, and the checks above found something wrong (also in %s).\n' "$SMOKE_LOG" >&2; exit 1
    fi
    # What to do next, last, where a person looks — the checks above are long and end on detail.
    printf '\n────────────────────────────────────────────────────────────\n'
    printf 'RouteMind is ready:  %s\n\n' "$BASE"
    printf '  Claude Code:  run `claude` in this directory and approve the "knowledge" server\n'
    printf '                (it asks once); /mcp then lists four tools.\n'
    printf '  Another agent: python3 mcp/knowledge_mcp.py   (reads the port from .env)\n'
    # An empty map had no next step anywhere: the screen said to click an area that did not exist.
    if [ "$(curl -fsS "$BASE/api/knowledge/regions" 2>/dev/null | python3 -c 'import json,sys; print(len(json.load(sys.stdin).get("regions") or []))' 2>/dev/null)" = 0 ]; then
      printf '\n  The map is empty. Open it, click the Back-Bone box, and choose "New AS" for your first\n'
      printf '  area — or start from the example: docs/DATA-REPO.md, "Starting over".\n'
    fi
    if grep -q '^KNOWLEDGE_AUTH=.\+' .env && ! grep -q '^KNOWLEDGE_AUTH=open' .env; then :; else
      printf '\n  Anyone who can reach this port can write to it (no login). docs/AUTH.md closes it.\n'
    fi
    printf '────────────────────────────────────────────────────────────\n'
    exit 0
  fi
  printf '.'; sleep 2; i=$((i+1))
done
printf '\nit did not come up. docker compose logs\n' >&2
exit 1
