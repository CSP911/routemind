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
  const steps = [
    ["1 — make the directories", "Its own repository, the way every backbone has one.", data.shell],
    ["2 — the secret, in .env", "One per member, used in both directions. That is what lets the exchange know who is calling.", data.env],
    [`3 — data-${data.name}/repo/peers.yaml`, "Its half of the declaration.", data.peers],
    [`4 — docker-compose.${data.name}.yml`, "A backbone of its own — repository, review queue, vocabulary.", data.compose],
  ];
  const frag = document.createDocumentFragment();
  for (const [title, why, text] of steps) {
    const d = el("div", "step");
    d.append(el("h3", null, title), el("p", null, why), el("pre", null, text));
    frag.append(d);
  }
  const last = el("div", "step");
  last.append(el("h3", null, "5 — register it above"),
              el("p", null, `Once it answers, add it as “${data.name}” at http://ontology-${data.name}:8100. Then decide, area by area, what it advertises — in its own screen, through its own review queue.`));
  frag.append(last);
  out.replaceChildren(frag);
});

load();
setInterval(load, 15000);
