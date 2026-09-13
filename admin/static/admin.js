"use strict";
// Small on purpose. This page reads a fact and hands over text; anything more belongs in the map,
// which is where an ontology is actually worked on.
const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };

async function api(path, body) {
  const r = await fetch(path, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {});
  return { ok: r.ok, data: await r.json().catch(() => ({})) };
}

async function load() {
  const { data } = await api("/api/state");
  const body = $("rows");
  const members = data.members || [];
  if (data.error || !members.length) {
    body.replaceChildren(el("tr", null, "")); 
    const td = el("td", "note", data.error || "Nobody is attached yet.");
    td.colSpan = 5; body.firstChild.append(td); return;
  }
  body.replaceChildren(...members.map((m) => {
    const tr = el("tr", m.reachable ? "up" : "down");
    const first = el("td");
    first.append(el("span", "dot"), document.createTextNode(m.label || m.name));
    // A room and a backbone are attached the same way and are not the same neighbour: one of them is
    // where knowledge starts, the other is a doorway to somebody else's. Worth a glance, not a column.
    if (m.kind === "exchange") first.append(el("span", "kind", "exchange"));
    tr.append(first, el("td", "mono", m.url));
    // "Advertising" is a count, never a list. What an area is, is between the members.
    tr.append(el("td", null, m.reachable ? `${m.advertising} area(s)` : "—"));
    tr.append(el("td", "rev", (m.revision || "").slice(0, 7) || "—"));
    const last = el("td");
    if (!m.reachable && m.error) last.append(el("div", "why", m.error));
    const drop = el("button", "link", "Remove");
    drop.addEventListener("click", async () => {
      if (!confirm(`Remove ${m.name} from this exchange? Its ontology is untouched; it simply stops meeting here.`)) return;
      await api("/api/members/remove", { name: m.name });
      load();
    });
    last.append(drop);
    tr.append(last);
    return tr;
  }));
}

$("addForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const msg = $("addMsg"); msg.className = "msg"; msg.textContent = "…";
  const { ok, data } = await api("/api/members", {
    name: $("mName").value.trim(), label: $("mLabel").value.trim(), url: $("mUrl").value.trim(),
    kind: $("mKind").value,
  });
  msg.className = ok ? "msg" : "msg bad";
  msg.textContent = ok ? `Registered. The room now holds: ${(data.members || []).join(", ")}`
                       : (data.error || "Could not register it.");
  if (ok) { $("addForm").reset(); load(); }
});

$("planForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const out = $("planOut"); out.replaceChildren(el("p", "note", "…"));
  const { ok, data } = await api("/api/plan", {
    name: $("pName").value.trim(), label: $("pLabel").value.trim(), port: Number($("pPort").value),
  });
  if (!ok) { out.replaceChildren(el("p", "msg bad", data.error || "Could not prepare it.")); return; }
  const list = [
    ["1 — make the directories", "Its own repository, the way every backbone has one.", data.shell],
    ["2 — the secret, in .env", "One per member, used in both directions. That is what lets the exchange know who is calling.", data.env],
    [`3 — data-${data.name}/repo/peers.yaml`, "Its half of the declaration.", data.peers],
    [`4 — docker-compose.${data.name}.yml`, "A backbone of its own — repository, review queue, vocabulary.", data.compose],
  ];
  list.push(["5 — register it above",
             `Once it answers, add it as “${data.name}” at http://ontology-${data.name}:8100. Then decide, area by area, what it advertises — in its own screen, through its own review queue.`, null]);
  steps(out, list);
});

function steps(out, list) {
  const frag = document.createDocumentFragment();
  for (const [title, why, text] of list) {
    const d = el("div", "step");
    d.append(el("h3", null, title), el("p", null, why));
    if (text) d.append(el("pre", null, text));
    frag.append(d);
  }
  out.replaceChildren(frag);
}

$("linkForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const out = $("linkOut"); out.replaceChildren(el("p", "note", "…"));
  const { ok, data } = await api("/api/plan", {
    kind: "exchange", name: $("xName").value.trim(), label: $("xLabel").value.trim(),
    url: $("xUrl").value.trim(), my_url: $("xMine").value.trim(),
  });
  if (!ok) { out.replaceChildren(el("p", "msg bad", data.error || "Could not prepare it.")); return; }
  steps(out, [
    ["1 — the secret, in .env here", "One for this link, used in both directions.", data.env],
    ["2 — your half of the declaration", `Or register “${data.name}” above with kind “another exchange”, which writes the same line.`, data.mine],
    [`3 — send these two to whoever runs ${data.label}`, "The same secret under the name their room looks it up by, and the entry naming this one. Send them the way you would send any shared secret — not in the same message as the address, and not anywhere it will be kept.", data.their_env + "\n" + data.theirs],
    ["4 — the link starts when they paste", "Until then this room simply reports it as unreachable, which is the honest answer: nobody is enrolled by one side alone."],
  ]);
});

load();
setInterval(load, 15000);
