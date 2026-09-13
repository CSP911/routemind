#!/bin/sh
# Every check in the tree, each in the environment it needs.
#
#   ./check/all.sh              against the install running at :8080
#   ./check/all.sh --quick      skip the slow ones (install-check, concurrency, llm-paths)
#   ./check/all.sh --only peer  just the ones whose name contains "peer"
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
for c in peer-check exchange-check ix-peering-check refresh-check room-check cross-check \
         domain-check admin-check overlay-check; do
  run "$c" $HOSTPY "check/$c.py"
done
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

printf '\n== the slow ones, which start services of their own ==\n'
if [ "$QUICK" = 1 ]; then
  printf '  (skipped by --quick: write-paths, llm-paths, install-check)\n'
else
  run write-paths sh check/write-paths.sh
  run llm-paths   sh check/llm-paths.sh
  if [ -z "$ONLY" ]; then
    printf '  install-check          not run here — it builds a clean clone and takes minutes.\n'
    printf '                         ./check/install-check.sh before a release.\n'
  fi
fi

printf '\npassed %s, failed %s%s\n' "$PASS" "$FAIL" "$([ "$FAIL" -gt 0 ] && printf ' —%s' "$FAILED")"
[ "$FAIL" -eq 0 ]
