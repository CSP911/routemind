#!/bin/sh
# What somebody who has never run this gets, walked end to end.
#
#   ./check/install-check.sh [--keep]
#
# Clones the **committed** tree into a temporary directory and installs it there: a first user gets
# what is in git, not what is in your working copy, and every defect this has found so far lived in
# that gap. Then it brings up the second backbone, wires both halves of the declaration, and walks
# the whole export decision — advertise, an audience, a line for one named reader, withdraw.
#
# Takes a few minutes because it builds. It is not part of the ordinary suite and should not be: run
# it before a release, and after a change large enough that you would not want to be the first person
# to find out. Five real defects came out of the first run, and three of them could not have come out
# of any check — a check builds its own world, and these were about the world a person arrives in:
# a key written twice in .env, a status code believed over a body, an IndexError where a sentence
# belonged.
#
# It touches nothing of yours. Its own directory, its own compose project, its own published ports,
# and its own IMAGE_TAG — the tags are shared, so a verification run that used the default would
# replace the images your install next starts from.
#
#   --keep   leave it running and print how to reach it. Otherwise everything, volumes included, goes.
set -e
cd "$(dirname "$0")/.."
ROOT="$(pwd)"

KEEP=0
[ "$1" = "--keep" ] && KEEP=1

PROJECT=routemind-install-check
TAG=install-check
WEB=8480; WEB_B=8481; ADMIN=8490
DIR="${TMPDIR:-/tmp}/$PROJECT.$$"
COMPOSE="-f docker-compose.yml -f docker-compose.peer.yml -f docker-compose.admin.yml"

fails=0
say()  { printf '%s\n' "$*"; }
ok()   { printf 'ok   %s\n' "$*"; }
bad()  { printf 'FAIL %s\n' "$*"; fails=$((fails+1)); }

cleanup() {
  # `--keep` keeps it whether or not it passed: the run you most want to poke at is the one that
  # failed, and tearing that down is throwing away the evidence.
  if [ "$KEEP" = "1" ]; then
    say ""
    say "left running, as asked:"
    say "  http://127.0.0.1:$WEB   this office      http://127.0.0.1:$WEB_B   the other"
    say "  http://127.0.0.1:$ADMIN   the exchange's operator screen"
    say "  $DIR"
    say "  take it down with:  cd $DIR && docker compose $COMPOSE down -v"
    [ "$fails" = "0" ] || say "  ($fails step(s) failed; install.log and up.log are in there)"
    return
  fi
  [ -d "$DIR" ] && ( cd "$DIR" && docker compose $COMPOSE down -v --remove-orphans >/dev/null 2>&1 ) || true
  rm -rf "$DIR"
}
trap cleanup EXIT INT TERM

command -v docker >/dev/null 2>&1 || { say "install-check needs docker"; exit 2; }
for p in $WEB $WEB_B $ADMIN; do
  if curl -fsS -o /dev/null "http://127.0.0.1:$p/" 2>/dev/null; then
    say "port $p is already answering. This check publishes on $WEB, $WEB_B and $ADMIN so it cannot"
    say "collide with an ordinary install; something else has one."
    exit 2
  fi
done

say "== a clone of what is committed, not of what is in the working copy =="
git -C "$ROOT" rev-parse --verify HEAD >/dev/null
git clone -q "$ROOT" "$DIR"
say "   $(git -C "$DIR" log --oneline -1)"
if [ -n "$(git -C "$ROOT" status --porcelain)" ]; then
  say "   (your working copy has uncommitted changes; they are deliberately not in this)"
fi

cd "$DIR"
cp .env.example .env
# Its own ports, its own image tags, and the two secrets an operator would generate. install.sh
# generates the first backbone's; the second backbone's and the operator door's are decisions.
sed -i.bak \
  -e "s/^WEB_PORT=8080\$/WEB_PORT=$WEB/" \
  -e "s/^#WEB_PORT_B=8081\$/WEB_PORT_B=$WEB_B/" \
  -e "s/^#ADMIN_PORT=8090\$/ADMIN_PORT=$ADMIN/" \
  -e "s/^#IMAGE_TAG=0.1.0\$/IMAGE_TAG=$TAG/" \
  -e "s/^#EXCHANGE_ADMIN_TOKEN=.*\$/EXCHANGE_ADMIN_TOKEN=install-check-operator/" \
  -e "s/^#EXCHANGE_TOKEN_BRANCH=.*\$/EXCHANGE_TOKEN_BRANCH=install-check-branch/" .env
rm -f .env.bak
for v in WEB_PORT WEB_PORT_B ADMIN_PORT IMAGE_TAG EXCHANGE_ADMIN_TOKEN EXCHANGE_TOKEN_BRANCH; do
  grep -q "^$v=" .env || bad "the .env.example line for $v is not where this expected it"
done

# The worked example, copied in before the first boot, exactly as the README says.
mkdir -p data/repo && cp -r examples/back-office/. data/repo/

say ""
say "== install.sh, as a first user runs it =="
if sh ./install.sh --no-llm > install.log 2>&1; then
  ok "it comes up and its own smoke passes ($(grep -c '^ok ' install.log) assertions, $(grep -c '^FAIL' install.log) failed)"
  grep -q '^FAIL' install.log && bad "install.sh's smoke reported failures — see $DIR/install.log"
else
  bad "install.sh exited non-zero — see $DIR/install.log"
  tail -20 install.log
  exit 1
fi

say ""
say "== the second backbone, wired the way docs/PEERING.md says =="
# Bind mounts docker would otherwise create owned by root, leaving a container that runs as
# KNOWLEDGE_UID unable to write them. The first run of this check is how that line reached the
# documents: it was in install.sh for the first backbone and in the operator screen's plan, and
# missing from the one command a person copies out of docs/PEERING.md.
mkdir -p data-b/repo data-b/publish data-b/overlays data-b/harness data-b/access
if ! docker compose $COMPOSE up -d > up.log 2>&1; then
  bad "the peer overlay did not come up"
  tail -12 up.log
  # A procedure that fails without saying why is the thing this procedure exists to catch.
  for svc in ontology-b web-b admin; do
    say ""; say "-- $svc --"; docker compose $COMPOSE logs --tail 25 "$svc" 2>&1 | tail -25
  done
  exit 1
fi
i=0; while [ $i -lt 60 ]; do
  curl -fsS -o /dev/null "http://127.0.0.1:$WEB_B/api/app-config" 2>/dev/null && break
  sleep 2; i=$((i+1))
done
# The backbone's half of the declaration. The exchange's half is added through the operator screen
# below, which is the half a person is told to add there.
cat > data-b/repo/peers.yaml <<'YAML'
peers:
  - name: ix
    label: EXCHANGE
    url: http://exchange:8110
    kind: exchange
    token_env: ONTOLOGY_PEER_TOKEN_IX
YAML
git -C data-b/repo add -A
git -C data-b/repo -c user.name=install-check -c user.email=i@l commit -qm "meet at the exchange"

say ""
say "== the walk =="
python3 "$ROOT/check/install-walk.py" "$WEB" "$WEB_B" "$ADMIN" || fails=$((fails+1))

say ""
if [ "$fails" = "0" ]; then say "a first install works, end to end"; else say "$fails step(s) failed"; fi
# Left behind on purpose — they are the build cache for the next run, and they are tagged apart from
# yours so nothing of yours is standing on them. Said rather than done quietly.
say "images tagged :$TAG are kept for the next run. Remove them with:"
say "  docker image rm knowledge-ontology:$TAG knowledge-web:$TAG routemind-exchange:$TAG routemind-admin:$TAG"
exit $([ "$fails" = "0" ] && echo 0 || echo 1)
