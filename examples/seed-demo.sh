#!/bin/sh
# Build the demonstration domain that docker-compose.demo.yml runs.
#
#   ./examples/seed-demo.sh
#   docker compose -f docker-compose.yml -f docker-compose.peer.yml \
#                  -f docker-compose.admin.yml -f docker-compose.demo.yml up -d --build
#
# Six backbones and two rooms, which is the smallest shape that shows every rule at once:
#
#   here          HOME     5 areas, one exchange (IX), one direct link that is down
#   one room out  BRANCH   payroll, on IX with HOME
#   two rooms out VENDOR   expense, procurement    ┐
#                 AUDIT    approval, payroll       ├ on PARTNER-IX, which meets IX as a peer room
#                 DEPOT    attendance              ┘
#   never up      LEGACY   a link HOME declares and nothing answers
#
# What each of those is there to show:
#   * a domain is one exchange and the backbones on it — HOME+BRANCH is one, the partner room another
#   * no transit: PARTNER-IX offers IX its own three members and never IX's, and vice versa
#   * an area crosses only if its representative has a `use_when_export` line — that is the whole
#     opt-in, and every area without one stays home
#   * `use_when_export_for` says it differently to one named peer (BRANCH does, to HOME)
#   * a link that is down suspends the absence rule, and looks different from one never configured —
#     which is why LEGACY has a token in .env.example it will never get to use
#
# The five ontologies are copies of examples/back-office with a peers.yaml and one export line each.
# They are not in git: 4.5 MB of the same worked example five times says nothing that these forty
# lines do not, and a copy in git is a copy that drifts from the original.
#
# Idempotent — it skips a repository that already exists, and never edits data/ twice.
set -e
cd "$(dirname "$0")/.."
say() { printf '%s\n' "$*"; }

[ -d examples/back-office ] || { say "examples/back-office is missing"; exit 1; }
IMAGE="knowledge-ontology:${IMAGE_TAG:-0.1.0}"

# `use_when_export` goes in the representative's frontmatter, just before its closing `---`. Written
# with awk rather than sed -i, whose in-place flag differs between GNU and BSD and quietly leaves
# a backup file on macOS.
export_line() {   # export_line <file> <line>
  f=$1; line=$2
  grep -q "^use_when_export:" "$f" && return 0
  awk -v add="$line" 'NR>1 && /^---$/ && !done { print add; done=1 } { print }' "$f" > "$f.new"
  mv "$f.new" "$f"
}

peers_file() {    # peers_file <dir> <room-name> <room-label> <host>
  cat > "$1/peers.yaml" <<EOF
# This backbone meets the others at one room, and names it here. The room names it back in its own
# members.yaml — both halves are needed, so nobody is enrolled by one side alone.
peers:
  - name: $2
    label: $3
    url: http://$4:8110
    kind: exchange
    token_env: ONTOLOGY_PEER_TOKEN_IX
EOF
}

backbone() {      # backbone <data-dir> <room-name> <room-label> <room-host>
  dir=$1
  if [ -d "$dir/repo/regions" ]; then say "--   $dir is already there, left alone"; return 0; fi
  mkdir -p "$dir/repo" "$dir/publish" "$dir/overlays" "$dir/harness" "$dir/access"
  cp -R examples/back-office/. "$dir/repo/"
  peers_file "$dir/repo" "$2" "$3" "$4"
  say "ok   $dir"
}

say "== the backbones =="
backbone data-b        ix         EXCHANGE   exchange
backbone data-vendor   partner-ix PARTNER-IX partner-ix
backbone data-audit    partner-ix PARTNER-IX partner-ix
backbone data-depot    partner-ix PARTNER-IX partner-ix

say "== what each one offers across a link =="
# One line per area that crosses. Everything else in each copy stays home, which is the default and
# the point: an area is not shared because it exists, it is shared because somebody wrote this line.
export_line data-b/repo/regions/payroll/payroll.md \
  'use_when_export: what this office pays and deducts · payslip lines · year-end papers'
# And the same area, said differently to one named peer.
grep -q "^use_when_export_for:" data-b/repo/regions/payroll/payroll.md || \
  awk '/^use_when_export:/ { print; print "use_when_export_for: {home: \"what the branch office pays and deducts, for head office to compare against its own\"}"; next } { print }' \
    data-b/repo/regions/payroll/payroll.md > data-b/repo/regions/payroll/payroll.md.new \
  && mv data-b/repo/regions/payroll/payroll.md.new data-b/repo/regions/payroll/payroll.md
export_line data-vendor/repo/regions/expense/expense.md \
  'use_when_export: what we invoice for and how · which receipts we attach'
export_line data-vendor/repo/regions/procurement/procurement.md \
  'use_when_export: which vendors we are registered with · what our forms ask · lead times we quote'
export_line data-audit/repo/regions/approval/approval.md \
  'use_when_export: which approvals we sample · what evidence an auditor asks for · retention we require'
export_line data-audit/repo/regions/payroll/payroll.md \
  'use_when_export: payroll figures we reconcile · the year-end papers we check'
export_line data-depot/repo/regions/attendance/attendance.md \
  'use_when_export: who is on shift at the depot · how a handover is logged'
say "ok   six areas offered, out of nineteen"

# regions.json is derived from those files and is also committed, so it has to be rebuilt here — the
# entrypoint git-inits and commits what it finds, it does not regenerate. README, "A hand-edited
# repository". Run in the image because it needs the service's own code and pyyaml.
say "== rebuilding the derived table =="
for d in data-b data-vendor data-audit data-depot; do
  docker run --rm -v "$PWD/$d/repo:/data/repo" -e PYTHONPATH=/app "$IMAGE" python3 -c \
    "import pathlib; from service.store import Store; from service.derive import regenerate; \
     print(regenerate(Store(pathlib.Path('/data/repo'))) or 'in sync')" | sed "s|^|  $d  |"
done

say "== the second room =="
mkdir -p data-partner-ix
if [ -f data-partner-ix/members.yaml ]; then say "--   already there, left alone"; else
cat > data-partner-ix/members.yaml <<'EOF'
# Who meets here. The token for each is in the environment, not in this file.
#
# This is the room's half of the declaration; each backbone names it in its own peers.yaml.
# Both halves are needed, so nobody is enrolled by one side alone.
members:
  - name: vendor
    label: VENDOR
    url: http://ontology-vendor:8100
    kind: backbone
    token_env: EXCHANGE_TOKEN_VENDOR
  - name: audit
    label: AUDIT
    url: http://ontology-audit:8100
    kind: backbone
    token_env: EXCHANGE_TOKEN_AUDIT
  - name: depot
    label: DEPOT
    url: http://ontology-depot:8100
    kind: backbone
    token_env: EXCHANGE_TOKEN_DEPOT
  # The other room. `kind: exchange` is what stops this one carrying its members on to a third.
  - name: ix
    label: IX
    url: http://exchange:8110
    kind: exchange
    token_env: EXCHANGE_TOKEN_PARTNER
EOF
say "ok   data-partner-ix/members.yaml"
fi

# ── and the two edits to your own install ─────────────────────────────────────
# Everything above is new directories. These two are not: they change the exchange you are already
# running and the backbone you are already reading. Guarded, and named out loud.
say "== your own domain =="
if [ ! -f data/exchange/members.yaml ]; then
  say "--   data/exchange/members.yaml is not there yet — start with docker-compose.exchange.yml first"
elif grep -q "name: partner-ix" data/exchange/members.yaml; then
  say "--   IX already knows the partner room"
else
  cat >> data/exchange/members.yaml <<'EOF'
  # The other room, as a member of this one. `kind: exchange` is the whole of the no-transit rule
  # from this side: a room offers a neighbour its own backbones and never a third room's.
  - name: partner-ix
    label: PARTNER-IX
    url: http://partner-ix:8110
    kind: exchange
    token_env: EXCHANGE_TOKEN_PARTNER
EOF
  say "ok   IX now meets the partner room"
fi

if [ ! -f data/repo/peers.yaml ]; then
  say "--   data/repo/peers.yaml is not there yet — link this backbone to IX first, docs/PEERING.md"
elif grep -q "name: legacy" data/repo/peers.yaml; then
  say "--   the down link is already declared"
else
  cat >> data/repo/peers.yaml <<'EOF'
  # A partner that never joined the room — a direct link, which is still a supported shape. It is
  # deliberately not running: a link this backbone declares is the only kind whose silence it can
  # see. A backbone that goes quiet behind an exchange just stops advertising, and from here that
  # is indistinguishable from it being gone.
  - name: legacy
    label: LEGACY
    url: http://ontology-legacy:8100
    token_env: EXCHANGE_TOKEN_LEGACY
EOF
  say "ok   the link that will never answer is declared"
  say "--   commit data/repo so the backbone is writable again: git -C data/repo commit -am 'the demo link'"
fi

say ""
say "Now: docker compose -f docker-compose.yml -f docker-compose.peer.yml \\"
say "                    -f docker-compose.admin.yml -f docker-compose.demo.yml up -d --build"
say "Then http://localhost:8080/knowledge — six cards on the wall, one of them not answering."
