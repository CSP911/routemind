#!/bin/sh
# Every check in the tree, each in the environment it needs.
#
#   ./check/all.sh              against the install running at :8080
#   ./check/all.sh --quick      skip the slow ones (install-check, concurrency, llm-paths)
#   ./check/all.sh --only walk  just the ones whose name contains "walk"
#
# There is no framework here and each check runs on its own; this only knows **where** each one can
# run, which is the part that is not obvious and was previously carried in somebody's head. Three
# environments, and no one of them satisfies all of them:
#
#   host                needs curl, or starts its own service, or is purely static
#   ontology container  needs pyyaml and the service's own modules
#   web container       needs fastapi and uvicorn
#
# It prints one line per suite and the count that suite reported. A suite that could not be run says
# so and fails the whole thing rather than being quietly skipped: a check that skips itself is worse
# than one that is not there. docs/CHECKS.md says what each of them proves.
set -u
cd "$(dirname "$0")/.."
BASE="${BASE:-http://127.0.0.1:8080}"
QUICK=0; ONLY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --quick) QUICK=1 ;;
    --only)  shift; ONLY="${1:-}" ;;
    *) printf 'unknown argument: %s\n' "$1"; exit 2 ;;
  esac
  shift
done

OUT=$(mktemp -d); trap 'rm -rf "$OUT"' EXIT
PASS=0; FAIL=0; FAILED=""

want() { [ -z "$ONLY" ] && return 0; case "$1" in *"$ONLY"*) return 0 ;; *) return 1 ;; esac; }

run() {   # run <name> <command...>
  name=$1; shift
  want "$name" || return 0
  printf '  %-22s' "$name"
  if "$@" >"$OUT/$name.log" 2>&1; then
    # Each check ends with its own count; show whatever it chose to say rather than inventing one.
    printf 'ok    %s\n' "$(grep -oE '[0-9]+ failed of [0-9]+|[0-9]+/[0-9]+|ok +[0-9]+ [a-z]+' "$OUT/$name.log" | tail -1)"
    PASS=$((PASS + 1))
  else
    printf 'FAIL\n'
    sed 's/^/      /' "$OUT/$name.log" | grep -E 'FAIL|Error|error|Traceback' | head -4
    printf '      (full output: %s)\n' "$OUT/$name.log"
    FAIL=$((FAIL + 1)); FAILED="$FAILED $name"
  fi
}

# ── does this python have pyyaml? several checks import the service ───────────
if python3 -c 'import yaml' 2>/dev/null; then
  HOSTPY=python3
else
  printf 'This python has no pyyaml, and the checks that import the service need it.\n'
  printf 'Either install it, or lift the pure-python copy out of the image:\n\n'
  printf '  docker compose cp ontology:/usr/local/lib/python3.12/site-packages/yaml ./pylib/yaml\n'
  printf '  rm -f ./pylib/yaml/_yaml*.so\n'
  printf '  PYTHONPATH=./pylib ./check/all.sh\n\n'
  printf 'docs/CHECKS.md, "Where each one can run".\n'
  exit 2
fi

cid() { docker compose ps -q "$1" 2>/dev/null; }
ONT=$(cid ontology); WEB=$(cid web)

printf '\n== on this machine, each starting what it needs ==\n'
run overlay-check $HOSTPY check/overlay-check.py
run ontology-check $HOSTPY ontology/check.py
[ "$QUICK" = 1 ] || run concurrency-check $HOSTPY check/concurrency-check.py

printf '\n== static: no server, no containers ==\n'
if command -v node >/dev/null 2>&1; then
  run css-check  node check/css-check.mjs
  run i18n-check node check/i18n-check.mjs
else
  printf '  %-22sFAIL  node is not installed, so three checks cannot run\n' "css/i18n/screen"
  FAIL=$((FAIL + 1)); FAILED="$FAILED node-missing"
fi
run env-check  $HOSTPY check/env-check.py
run eol-check  $HOSTPY check/eol-check.py
run romanize   $HOSTPY check/romanize-check.py
# Invariant 10: nothing secret-shaped in any tracked file — the pre-push grep, as a check.
run secrets    $HOSTPY check/secrets-check.py
# Every path the MCP server calls has a route on the web app .mcp.json points it at.
run mcp-routes $HOSTPY check/mcp-routes-check.py
  # The circuit's client against far ends that misbehave: a redirect, no key, a wrong address.
  run circuit-client $HOSTPY check/circuit-client-check.py
# The two times on a routing row. It builds its own repository and commits into it, so it needs git
# and nothing else — no service, no containers.
run age        $HOSTPY check/age-check.py
# What an edit by hand leaves behind. Needs the service's own modules, so it runs wherever those
# import — the same condition as the other static ones.
run tidy       $HOSTPY check/tidy-check.py

printf '\n== in the containers ==\n'
if [ -n "$ONT" ]; then
  # `docker cp` copies *into* an existing directory, so a stale file survives and you run it
  # believing it is the one you just edited. Remove first, every time.
  docker exec -i "$ONT" rm -rf /tmp/check /tmp/mcp >/dev/null 2>&1
  docker cp check "$ONT:/tmp/check" >/dev/null && docker cp mcp "$ONT:/tmp/mcp" >/dev/null
  run scenarios docker exec -i "$ONT" python3 /tmp/check/scenarios.py
else
  printf '  %-22sFAIL  no ontology container is running (docker compose up -d)\n' "scenarios"
  FAIL=$((FAIL + 1)); FAILED="$FAILED scenarios"
fi
if [ -n "$WEB" ]; then
  docker exec -i "$WEB" rm -rf /tmp/check >/dev/null 2>&1
  docker cp check "$WEB:/tmp/check" >/dev/null
  run auth-check docker exec -i "$WEB" python3 /tmp/check/auth-check.py
else
  printf '  %-22sFAIL  no web container is running\n' "auth-check"
  FAIL=$((FAIL + 1)); FAILED="$FAILED auth-check"
fi

printf '\n== against the install at %s ==\n' "$BASE"
run smoke     sh check/smoke.sh "$BASE"
run mcp-check $HOSTPY check/mcp-check.py "$BASE/api/knowledge"
# A circuit into this install, the way another backbone opens one: through the web port, with the key.
# The key comes from the environment or from the same .env compose reads — under its current name, or
# the one an install made before 2026-10-08 still has. Not skipped when it is missing: a suite that
# cannot run says so and fails.
CIRCUIT_TOKEN="${KNOWLEDGE_CIRCUIT_TOKEN:-}"
[ -n "$CIRCUIT_TOKEN" ] || CIRCUIT_TOKEN=$(sed -n 's/^KNOWLEDGE_CIRCUIT_TOKEN=//p' .env 2>/dev/null | tail -1)
[ -n "$CIRCUIT_TOKEN" ] || CIRCUIT_TOKEN=$(sed -n 's/^EXCHANGE_TOKEN_HOME=//p' .env 2>/dev/null | tail -1)
ROUTEMIND_TOKEN="$CIRCUIT_TOKEN" run circuit $HOSTPY check/circuit-check.py "$BASE"
# The session tokens, run inside the ontology against itself: that service publishes no port, which
# is the design — the web proxy is the only way in from outside — so this is where it is reachable.
if [ -n "$ONT" ]; then
  docker cp check/session-check.py "$ONT:/tmp/session-check.py" >/dev/null 2>&1
  run session docker exec -i -e ROUTEMIND_TOKEN="$CIRCUIT_TOKEN" \
      -e ROUTEMIND_API=http://127.0.0.1:8100 "$ONT" python3 /tmp/session-check.py
fi

printf '\n== the slow ones, which start services of their own ==\n'
if [ "$QUICK" = 1 ]; then
  printf '  (skipped by --quick: write-paths, llm-paths, place, install-check)\n'
else
  run write-paths sh check/write-paths.sh
  run llm-paths   sh check/llm-paths.sh
  # Placing a document by walking the table, through the MCP, with the write and the queued
  # proposal read back. Starts an ontology on a copy of the shipped corpus, so it sits here.
  run place       $HOSTPY check/place-check.py
  # A change set (docs/CHANGE.md): several decisions, one commit, the lines over them decided; the
  # preview is the write without the commit; through the API and through the MCP's `here`.
  run change      $HOSTPY check/change-check.py
  # What a non-expert meets: size budgets as warnings, names among siblings, no silent overwrite, the
  # review queue saying what happened, named refusals, stale sets (2026-10-10 B2C pass).
  run b2c         $HOSTPY check/b2c-check.py
  # A hand-edited repository, served: a stale regions.json regenerated at startup when the tree is
  # clean, the files' truth served when it is not. Starts its own ontology twice.
  run drift       $HOSTPY check/drift-check.py
  # Invariants 1 and 2 at the agent's door: every walk starts at hop 0, "not here" only with the
  # whole list seen. Drives the MCP server over stdio against an ontology it starts.
  run walk        $HOSTPY check/walk-check.py
  # Invariant 4: every reader of one fact gets the same answer. Every fact × every path, on a clean
  # tree and again with an uncommitted hand edit. Starts its own ontology and an MCP.
  run same-answer $HOSTPY check/same-answer-check.py
  # Invariants 5 and 7: every write path — API, proposal accept, tidy — a success
  # and a failure each, with commits and tree state read back. Starts its own ontologies.
  run transact    $HOSTPY check/transact-check.py
  # Invariant 3, the derived state that is not a file: what a circuit reads, its session, and the
  # MCP's area list each follow their source without waiting out a timer. Two backbones, an MCP.
  run follow      $HOSTPY check/follow-check.py
  # An area with a hyphen in its directory, on every path that once spelled it two ways (user report 2026-10-07).
  run hyphen      $HOSTPY check/hyphen-check.py
  # Invariant 11: every walk recorded, the screen and the agent reading the same record — the
  # store, the service and an agent through the MCP; then the real page polling and replaying it.
  run footprint   $HOSTPY check/footprint-check.py
  if command -v node >/dev/null 2>&1; then run footprint-screen $HOSTPY check/footprint-screen-check.py; fi
  if [ -z "$ONLY" ]; then
    printf '  install-check          not run here — it builds a clean clone and takes minutes.\n'
    printf '                         ./check/install-check.sh before a release.\n'
  fi
fi

printf '\npassed %s, failed %s%s\n' "$PASS" "$FAIL" "$([ "$FAIL" -gt 0 ] && printf ' —%s' "$FAILED")"
[ "$FAIL" -eq 0 ]
