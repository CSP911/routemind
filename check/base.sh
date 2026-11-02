# The install in this checkout, for a check given no address. Sourced, not run:
#
#   . "$ROOT/check/base.sh"; BASE="${1:-$(checkout_base "$ROOT")}"
#
# Every check that talks to "the install" defaulted to :8080, so from a checkout installed on another
# port it tested — and llm-paths wrote into — whatever RouteMind held 8080, and passed (quickstart
# QS-1, suite CS-1, docs DC-2, 2026-11-02). The port is read the way install.sh and docker compose read
# it: the **last** WEB_PORT line in .env, quotes and spaces trimmed. 8080 only when .env names none.
# check/env-check.py runs this against a .env that names the port twice.
checkout_base() {
  _port="$(grep -E '^[[:space:]]*WEB_PORT=' "$1/.env" 2>/dev/null | tail -n 1 | cut -d= -f2- | tr -d '"'"'"' \r' | tr -d '[:space:]')"
  printf 'http://127.0.0.1:%s\n' "${_port:-8080}"
}
